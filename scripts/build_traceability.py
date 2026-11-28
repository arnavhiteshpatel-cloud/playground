#!/usr/bin/env python3
"""Build docs/quality/traceability_matrix.csv from the requirement -> test mapping held in this file.

The mapping below is the single source of the matrix. Each row links one functional specification
item (FS) of docs/quality/FUNCTIONAL_SPEC.md, and through it one requirement (URS) of
docs/quality/URS.md, to the automated tests and other evidence that verify it.

Status rules (applied by the author of a row, checked by this script):
  VERIFIED  an automated test in tests/ asserts the specified behaviour.
  PARTIAL   a test exists but does not assert the whole behaviour (for example it exercises the
            function without asserting the audit event, or covers the library but not the desktop
            path), or the only evidence is a recorded manual/scripted procedure (e.g. an experiment
            script or a pip-audit output) rather than a test in the suite.
  GAP       no test and no recorded procedure. A protocol step written during the re-baseline
            (OQ_PROTOCOL.md) does not count as evidence until it has been executed.

Checks performed:
  1. every referenced test exists in `pytest --collect-only -q` output (parametrised ids are
     reduced to file::function);
  2. every referenced evidence file exists;
  3. status consistency (VERIFIED needs >= 1 test; PARTIAL needs a test or evidence; GAP has no
     tests and names a proposed test or review);
  4. the URS and FS ids in the documents match the mapping (retired ids excluded);
  5. every protocol reference occurs in IQ_PROTOCOL.md or OQ_PROTOCOL.md.

This is an engineering traceability record. It is not a validation record and supports no
compliance claim.

Usage:
  python scripts/build_traceability.py            # check, then write the CSV and print counts
  python scripts/build_traceability.py --check    # check only; exit 1 if the CSV on disk differs
  python scripts/build_traceability.py --no-collect   # skip pytest collection (faster, weaker)
"""
from __future__ import annotations

import argparse
import collections
import csv
import io
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QDIR = ROOT / "docs" / "quality"
CSV_PATH = QDIR / "traceability_matrix.csv"
COLUMNS = ["URS", "FS", "area", "status", "tests", "other_evidence", "test_level", "risk_ids",
           "protocol_ref", "notes", "proposed_test"]

# Requirements retired in the Generation-2 re-baseline (see URS.md section 5 / FS.md section 3).
RETIRED_URS = {"URS-012", "URS-130"}
RETIRED_FS = {"FS-012-1", "FS-012-2", "FS-130-1"}

D = "tests/desktop/"
TG = D + "test_traceability_gaps.py::"
TGL = "tests/test_traceability_gaps_library.py::"


@dataclass
class Row:
    urs: str
    fs: str
    area: str
    status: str
    tests: list = field(default_factory=list)
    evidence: list = field(default_factory=list)
    level: str = "unit"
    risks: str = ""
    protocol: str = ""
    notes: str = ""
    proposed: str = ""


V, P, G = "VERIFIED", "PARTIAL", "GAP"

ROWS: list[Row] = [
    # ------------------------------------------------------------------ 3.1 general
    Row("URS-001", "FS-001-1", "general", P, [D + "test_main_window.py::test_about_lists_third_party_licences"],
        level="system", risks="RSK-34", protocol="OQ-GEN-01",
        notes="About dialog is constructed but its RUO / not-validated text is not asserted",
        proposed="test_about_and_start_page_show_ruo_statement"),
    Row("URS-001", "FS-001-2", "general", V, ["tests/test_controls.py::test_report_contains_ruo_and_not_validated_statements",
                                               "tests/test_report_bounds.py::test_pdf_banner_and_bounds",
                                               D + "test_timepoint_dataclass.py::test_synthetic_demo_report_is_labelled_synthetic",
                                               TGL + "test_every_pdf_and_csv_carry_ruo_data_class_and_review_status",
                                               TG + "test_pdf_and_csv_text_contain_ruo_statement"],
        level="integration", risks="RSK-34", protocol="OQ-GEN-01",
        notes="rendered PDF text: full RUO / not-validated statement on page 1 and the RUO footer on every page, for "
              "every data class and both review statuses and for the desktop report; CSV header and every row carry "
              "the data class and the review status (unreviewed_automated, then reviewed after approval)"),
    Row("URS-002", "FS-002-1", "general", P, ["tests/test_analysis_modules.py::test_cli_commands"],
        level="integration", risks="RSK-18", protocol="OQ-GEN-02",
        notes="software_version asserted in the analysis JSON only; PDF, measurement row and About not asserted",
        proposed="test_pdf_measurement_and_about_embed_same_version"),
    # ------------------------------------------------------------------ 3.2 access control
    Row("URS-010", "FS-010-1", "access", P, [D + "test_admin_lock_audit.py::test_user_admin_add_deactivate_reset_audited"],
        level="integration", risks="RSK-23", protocol="OQ-ACC-01",
        notes="duplicate user name refused ('already taken') in the desktop; ids never reused and the absence of a "
              "delete path are not tested",
        proposed="test_duplicate_username_rejected_and_ids_not_reused"),
    Row("URS-010", "FS-010-2", "access", V, [D + "test_services.py::test_project_create_open_login"],
        level="integration", risks="RSK-23", protocol="OQ-ACC-01",
        notes="new project creates a named administrator; weak password refused; no default account"),
    Row("URS-010", "FS-010-3", "access", V, [D + "test_admin_lock_audit.py::test_user_admin_add_deactivate_reset_audited",
                                              D + "test_cycle2_fixes.py::test_c2_08_self_service_password_change",
                                              D + "test_cycle2_fixes.py::test_c2_09_role_change_audited_and_database_edit_detected"],
        level="system", risks="RSK-23", protocol="OQ-ACC-02",
        notes="Users dialog adds named users with a role, changes roles, deactivates/reactivates (sign-in refused) and "
              "resets passwords; non-admins refused; user.create/activate/deactivate asserted, user.role_change asserted "
              "on Project.set_user_role, which the dialog calls"),
    Row("URS-011", "FS-011-1", "access", V, ["tests/test_api.py::test_rbac_and_tenant_isolation",
                                              "tests/test_security_gen2.py::test_writes_require_write_permission",
                                              "tests/test_store_api_workflows.py::test_store_lookup_errors_and_roles"],
        level="unit", risks="RSK-24", protocol="OQ-ACC-03",
        notes="store-level permission matrix (desktop calls the same Store methods)"),
    Row("URS-011", "FS-011-2", "access", P, [D + "test_review_fixes.py::test_ux10_actions_disabled_by_role_with_reason",
                                              D + "test_review_fixes.py::test_ux10_analyst_cannot_sign",
                                              D + "test_cycle2_fixes.py::test_c2_03_reviewer_cannot_switch_blinded_mode_off"],
        level="system", risks="RSK-24", protocol="OQ-ACC-03",
        notes="reviewer: import/analysis/ROI/editing/user actions disabled with reason, signing enabled; analyst: editing "
              "enabled, signing disabled; Audit-trail tab visibility by role and the viewer role are not asserted",
        proposed="test_desktop_actions_follow_role_permissions"),
    Row("URS-013", "FS-013-1", "access", V, ["tests/test_api.py::test_password_policy_and_lockout",
                                              D + "test_services.py::test_project_create_open_login"],
        risks="RSK-23", protocol="OQ-ACC-04",
        notes="policy >=10 chars, upper case, digit; scrypt N=2^14 is below current OWASP guidance (G2-18)"),
    Row("URS-013", "FS-013-2", "access", V, ["tests/test_api.py::test_password_policy_and_lockout",
                                              "tests/test_security_fixes.py::test_S09_lockout_is_temporary"],
        risks="RSK-23", protocol="OQ-ACC-04", notes="5 failures -> 15 min temporary lock"),
    Row("URS-013", "FS-013-3", "access", V, [D + "test_admin_lock_audit.py::test_idle_lock_hides_project_and_unlock_uses_lockout",
                                              D + "test_cycle2_fixes.py::test_c2_02_idle_lock_blocks_every_window_and_dialog"],
        level="system", risks="RSK-23", protocol="OQ-ACC-05",
        notes="default 15 min, configurable (audited settings.idle_lock); lock hides the project and blocks input to every "
              "window; unlock needs the password and counts towards lockout"),
    Row("URS-014", "FS-014-1", "access", P, ["tests/test_security_gen2.py::test_deactivation_deletes_sessions_and_login_purges_expired",
                                              "tests/test_security_gen2.py::test_reauthentication_inactive_user",
                                              D + "test_admin_lock_audit.py::test_user_admin_add_deactivate_reset_audited",
                                              D + "test_cycle2_fixes.py::test_c2_07_deactivated_user_session_ends_at_next_action",
                                              D + "test_cycle2_fixes.py::test_c2_07_window_signs_out_deactivated_user"],
        level="integration", risks="RSK-23", protocol="OQ-ACC-06",
        notes="deactivation from the desktop ends the session at the next action and blocks sign-in and unlock; "
              "absence of a user delete path not tested",
        proposed="test_no_user_delete_path_and_history_keeps_user"),
    Row("URS-015", "FS-015-2", "access", V, [D + "test_services.py::test_review_requires_reauth_and_separation_of_duties",
                                              "tests/test_controls.py::test_author_cannot_approve_own_segmentation",
                                              "tests/test_store_api_workflows.py::test_reviews_on_reports_and_unknown_objects"],
        level="integration", risks="RSK-26", protocol="OQ-SIG-04"),
    Row("URS-015", "FS-015-1", "access", G, level="unit", risks="RSK-20;RSK-24", protocol="OQ-ACC-07",
        notes="admin role is a superset (write, run, review, unblind, delete); no separation of system administration",
        proposed="test_admin_role_cannot_analyse_or_sign_without_recorded_justification"),
    Row("URS-016", "FS-016-1", "access", V, ["tests/test_store_api_workflows.py::test_admin_user_management_endpoints",
                                              "tests/test_security_gen2.py::test_deactivation_deletes_sessions_and_login_purges_expired",
                                              D + "test_admin_lock_audit.py::test_user_admin_add_deactivate_reset_audited",
                                              D + "test_cycle2_fixes.py::test_c2_09_role_change_audited_and_database_edit_detected"],
        level="integration", risks="RSK-23", protocol="OQ-ACC-06",
        notes="user.create, user.activate, user.deactivate asserted; user.role_change asserted with old and new role"),
    Row("URS-017", "FS-017-1", "access", G, level="procedure", risks="RSK-20;RSK-48", protocol="IQ-06",
        notes="user-organisation control (OS permissions on the project folder); IQ step not executed",
        proposed="IQ-06 execution record"),
    # ------------------------------------------------------------------ 3.3 ingestion
    Row("URS-020", "FS-020-1", "ingestion", V, [D + "test_import.py::test_slab_import_matches_full_import",
                                                 "tests/test_io_destructive.py::test_large_stack_uses_manifest_hash",
                                                 "tests/test_io_properties.py::test_zarr_roundtrip_exact_with_hash"],
        level="integration", risks="RSK-04", protocol="OQ-ING-01"),
    Row("URS-020", "FS-020-2", "ingestion", G, level="integration", risks="RSK-04", protocol="OQ-ING-01",
        notes="by design the stored image array is written once at import; no test asserts it is never rewritten",
        proposed="test_stored_image_array_unchanged_after_analysis_and_edits"),
    Row("URS-021", "FS-021-1", "ingestion", P, ["tests/test_io_destructive.py::test_zarr_integrity_detects_deleted_chunk"],
        level="integration", risks="RSK-04", protocol="OQ-ING-02",
        notes="library read verifies content hash; no desktop test that a tampered project store blocks QC/analysis",
        proposed="test_tampered_project_store_blocks_analysis"),
    Row("URS-021", "FS-021-2", "ingestion", G, level="integration", risks="RSK-04", protocol="OQ-ING-02",
        notes="not implemented: no on-demand project integrity check", proposed="test_verify_project_integrity_reports_and_audits"),
    Row("URS-022", "FS-022-1", "ingestion", P, [D + "test_import.py::test_probe_formats",
                                                 "tests/test_io_metadata.py::test_txm_recon_fields_and_tuple_pixel_size",
                                                 "tests/test_io_metadata.py::test_dicom_multiframe_and_metadata",
                                                 "tests/test_core.py::test_tiff_without_spacing_warns"],
        level="unit", risks="RSK-01", protocol="OQ-ING-03",
        notes="spacing source and format metadata tested; acquisition fields not uniform across formats and not printed in report (CRO-06)",
        proposed="test_acquisition_metadata_null_not_defaulted_all_formats"),
    Row("URS-023", "FS-023-1", "ingestion", V, [D + "test_import.py::test_spacing_validation",
                                                 "tests/test_core.py::test_volume_rejects_bad_spacing"],
        risks="RSK-01;RSK-02", protocol="OQ-ING-04"),
    Row("URS-023", "FS-023-2", "ingestion", V, [D + "test_import.py::test_model_requires_explicit_spacing",
                                                 D + "test_import.py::test_wizard_pages_offscreen",
                                                 "tests/test_io_properties.py::test_user_spacing_override_is_recorded"],
        level="integration", risks="RSK-01", protocol="OQ-ING-04"),
    Row("URS-024", "FS-024-1", "ingestion", G, level="integration", risks="RSK-04", protocol="OQ-ING-01",
        notes="by design import copies into the project store; source immutability not tested",
        proposed="test_import_leaves_source_files_byte_identical"),
    Row("URS-025", "FS-025-1", "ingestion", V, [D + "test_import.py::test_run_assigns_and_logs_rejections",
                                                 D + "test_import.py::test_duplicate_is_rejected_with_reason"],
        level="integration", risks="RSK-03", protocol="OQ-ING-05"),
    Row("URS-025", "FS-025-2", "ingestion", G, level="integration", risks="RSK-03", protocol="OQ-ING-05",
        notes="not implemented: second scan for the same animal/timepoint is not flagged",
        proposed="test_second_scan_same_animal_timepoint_requires_confirmation"),
    Row("URS-026", "FS-026-1", "ingestion", V, [D + "test_import.py::test_run_assigns_and_logs_rejections",
                                                 D + "test_import.py::test_probe_formats"],
        level="integration", risks="RSK-04", protocol="OQ-ING-06"),
    Row("URS-026", "FS-026-2", "ingestion", V, ["tests/test_io_destructive.py::test_truncation_never_crashes",
                                                 "tests/test_io_destructive.py::test_random_byte_mutations_never_crash",
                                                 "tests/test_io_destructive.py::test_detect_format_errors"],
        risks="RSK-45", protocol="OQ-ING-06"),
    # ------------------------------------------------------------------ 3.4 QC
    Row("URS-030", "FS-030-1", "qc", P, [D + "test_import.py::test_qc_failure_is_flagged_not_dropped",
                                          D + "test_import.py::test_run_assigns_and_logs_rejections",
                                          "tests/test_properties_science.py::test_qc_never_crashes_on_degenerate_volumes",
                                          "tests/test_core.py::test_tiff_stack_missing_slice_detection"],
        level="integration", risks="RSK-05;RSK-36", protocol="OQ-QC-01",
        notes="deterministic checks verified; heuristic thresholds (rings, cupping, CNR) are developer-chosen and unvalidated",
        proposed="test_heuristic_qc_checks_against_reference_artefact_phantoms"),
    Row("URS-031", "FS-031-1", "qc", P, [D + "test_import.py::test_run_assigns_and_logs_rejections"],
        level="unit", risks="RSK-05", protocol="OQ-QC-01",
        notes="check basis asserted; stored qc_version, thresholds and decimation note not asserted",
        proposed="test_qc_record_stores_version_threshold_value_and_decimation"),
    Row("URS-032", "FS-032-1", "qc", G, level="integration", risks="RSK-05", protocol="OQ-QC-02",
        notes="not implemented: QC verdict 'unsuitable' flags the scan but does not block analysis",
        proposed="test_unsuitable_scan_blocks_analysis_unless_override_with_reason"),
    # ------------------------------------------------------------------ 3.5 ROI
    Row("URS-040", "FS-040-1", "roi", V, ["tests/test_transforms_roi.py::test_roi_serialisation_hash_and_revision",
                                           "tests/test_transforms_roi.py::test_cylinder_mask_volume_matches_analytic",
                                           "tests/test_core.py::test_cylinder_roi_volume_and_hash",
                                           D + "test_services.py::test_manual_roi_then_analysis"],
        risks="RSK-06", protocol="OQ-ROI-01"),
    Row("URS-041", "FS-041-1", "roi", V, [D + "test_services.py::test_manual_roi_then_analysis",
                                           D + "test_cycle2_fixes.py::test_c2_17_manual_roi_needs_reason_and_second_person",
                                           TG + "test_manual_roi_requires_reason_and_is_audited"],
        level="integration", risks="RSK-06", protocol="OQ-ROI-02",
        notes="roi.save asserted for the automatic and the manual ROI (scan, version, definition hash, method, reason); "
              "the ROI dialog and the service refuse a missing or short reason and then store and audit nothing"),
    Row("URS-042", "FS-042-1", "roi", P, [D + "test_main_window.py::test_open_project_view_scan_edit_and_save",
                                           D + "test_main_window.py::test_oblique_reslice_identity",
                                           D + "test_review_fixes.py::test_ux01_roi_drawn_in_slice_views_and_3d"],
        level="system", risks="RSK-06;RSK-36", protocol="OQ-ROI-03",
        notes="views render and link; ROI overlay asserted in the axial view and the 3D panel, not in the coronal and "
              "sagittal views", proposed="test_roi_overlay_visible_in_three_planes"),
    Row("URS-042", "FS-042-2", "roi", V, [D + "test_review_fixes.py::test_ux02_accept_roi_is_signed_audited_and_clears_flag",
                                           D + "test_review_fixes.py::test_ux02_review_panel_accept_and_edit_buttons",
                                           D + "test_cycle2_fixes.py::test_c2_17_manual_roi_needs_reason_and_second_person"],
        level="system", risks="RSK-06", protocol="OQ-ROI-03",
        notes="results stay 'ROI not yet accepted' until a second person signs the ROI (review.approved with the ROI "
              "definition hash); the ROI author cannot accept it"),
    # ------------------------------------------------------------------ 3.6 segmentation and editing
    Row("URS-050", "FS-050-1", "segmentation", P, ["tests/test_analysis_modules.py::test_compose_three_class_semantics",
                                                    D + "test_editing.py::test_invalid_label_rejected"],
        risks="RSK-08", protocol="OQ-SEG-01",
        notes="label semantics tested; the label map is not stored with each result",
        proposed="test_label_map_stored_with_every_segmentation"),
    Row("URS-051", "FS-051-1", "segmentation", P, ["tests/test_ml_phantom.py::test_pipeline_unet_and_onnx_paths_record_model_identity"],
        level="integration", risks="RSK-10", protocol="OQ-SEG-01",
        notes="model SHA-256 recorded; preprocessing configuration not recorded separately",
        proposed="test_segmentation_record_contains_model_hash_and_preprocessing"),
    Row("URS-052", "FS-052-1", "segmentation", V, [D + "test_services.py::test_label_revision_audit",
                                                    "tests/test_api.py::test_end_to_end",
                                                    D + "test_main_window.py::test_open_project_view_scan_edit_and_save",
                                                    D + "test_review_fixes.py::test_ux06_version_detail_and_compare_overlay",
                                                    D + "test_cycle2_fixes.py::test_c2_10_cancelled_or_failed_revision_leaves_nothing",
                                                    TG + "test_automatic_prediction_is_version_1_and_base_labels_unchanged"],
        level="integration", risks="RSK-13", protocol="OQ-SEG-03",
        notes="version 1 is kind=automatic without parent; each correction is a new corrected version with its parent "
              "under a new labels key; the stored arrays of earlier versions re-read unchanged (and match their hash)"),
    Row("URS-053", "FS-053-1", "segmentation", V, [D + "test_services.py::test_label_revision_audit",
                                                    "tests/test_controls.py::test_correction_requires_reason"],
        level="integration", risks="RSK-13", protocol="OQ-SEG-03"),
    Row("URS-054", "FS-054-1", "segmentation", V, [D + "test_editing.py::test_invalid_label_rejected",
                                                    D + "test_services.py::test_label_revision_audit"],
        risks="RSK-08", protocol="OQ-SEG-02"),
    Row("URS-054", "FS-054-2", "segmentation", G, level="unit", risks="RSK-08", protocol="OQ-SEG-02",
        notes="pipeline checks class count (ARC-06) but not the label-map mapping; report legend is hard-coded",
        proposed="test_model_load_rejects_permuted_label_map"),
    Row("URS-055", "FS-055-1", "segmentation", V, ["tests/test_analysis_modules.py::test_entropy_mi_abstain_and_plausibility",
                                                    "tests/test_core.py::test_abstain_excluded",
                                                    D + "test_services.py::test_measurement_support_statuses"],
        risks="RSK-09;RSK-11", protocol="OQ-SEG-04"),
    Row("URS-056", "FS-056-1", "editing", V, [D + "test_editing.py::test_protect_other_classes",
                                               D + "test_editing.py::test_eraser_only_active_class",
                                               D + "test_editing.py::test_anisotropic_brush_is_round_in_physical_space",
                                               D + "test_editing.py::test_stroke_is_continuous_and_single_diff",
                                               D + "test_editing.py::test_region_grow_2d_and_3d",
                                               D + "test_editing.py::test_fill_holes",
                                               D + "test_editing.py::test_interpolation_between_key_slices"],
        risks="RSK-47", protocol="OQ-EDT-01"),
    Row("URS-056", "FS-056-2", "editing", V, [D + "test_editing.py::test_undo_stack_random_sequence",
                                               D + "test_editing.py::test_sparse_diff_roundtrip_and_compression",
                                               D + "test_editing.py::test_class_delta_and_change_summary",
                                               D + "test_editing.py::test_viewer_state_edit_flow"],
        risks="RSK-47", protocol="OQ-EDT-02"),
    # ------------------------------------------------------------------ 3.7 morphometry
    Row("URS-060", "FS-060-1", "morphometry", P, ["tests/test_morphometry_analytic.py::test_defect_report_metrics_iso_and_anisotropic",
                                                   "tests/test_morphometry_analytic.py::test_class_volumes_additivity_and_abstention",
                                                   "tests/test_core.py::test_class_volumes_and_bridging"],
        evidence=["docs/science/ENDPOINT_DEFINITIONS.md"], risks="RSK-14", protocol="OQ-MOR-01",
        notes="definitions documented; no metric registry in code; endpoint-definition findings BIO-10/BIO-11 open",
        proposed="test_metric_registry_matches_endpoint_definitions"),
    Row("URS-061", "FS-061-1", "morphometry", P, [D + "test_services.py::test_label_revision_audit"],
        level="integration", risks="RSK-14;RSK-27", protocol="OQ-MOR-01",
        notes="measurement row links segmentation, ROI and software version; config_id is not populated",
        proposed="test_measurement_row_links_seg_roi_config_and_version"),
    Row("URS-062", "FS-062-1", "morphometry", V, ["tests/test_morphometry_analytic.py::test_volume_is_voxel_count_times_voxel_volume_anisotropic",
                                                   "tests/test_morphometry_analytic.py::test_plate_thickness_even_is_exact",
                                                   "tests/test_morphometry_analytic.py::test_plate_thickness_odd_has_documented_plus_one_voxel_bias",
                                                   "tests/test_morphometry_analytic.py::test_trabecular_morphometry_on_plates_exact",
                                                   "tests/test_morphometry_analytic.py::test_surface_area_cube_and_sphere_marching_cubes",
                                                   "tests/test_properties_science.py::test_measures_scale_with_voxel_size",
                                                   "tests/test_core.py::test_plate_thickness_and_bvtv",
                                                   "tests/test_core.py::test_sphere_volume_and_surface"],
        evidence=["experiments/results/exp_G_morphometry.json"], risks="RSK-14;RSK-01;RSK-02", protocol="OQ-MOR-02"),
    Row("URS-063", "FS-063-1", "morphometry", V, ["tests/test_controls.py::test_density_suppressed_without_calibration",
                                                   "tests/test_advisor.py::test_density_requires_calibration"],
        risks="RSK-15", protocol="OQ-MOR-03"),
    # ------------------------------------------------------------------ 3.8 statistics and blinding
    Row("URS-070", "FS-070-1", "statistics", G, level="integration", risks="RSK-16", protocol="OQ-STA-01",
        notes="not implemented: no statistical analysis plan object or lock", proposed="test_sap_lock_immutable_and_amendment_versioned"),
    Row("URS-070", "FS-070-2", "statistics", G, level="integration", risks="RSK-16", protocol="OQ-STA-01",
        notes="not implemented", proposed="test_unblinding_requires_locked_sap"),
    Row("URS-071", "FS-071-2", "statistics", V, ["tests/test_stats_reference.py::test_icc_matches_shrout_fleiss",
                                                  "tests/test_stats_reference.py::test_adjust_pvalues_matches_statsmodels",
                                                  "tests/test_stats_reference.py::test_bland_altman_constructed",
                                                  "tests/test_stats_reference.py::test_hedges_g_known_value_and_symmetry",
                                                  "tests/test_stats_reference.py::test_bootstrap_ci_contains_mean_and_is_deterministic"],
        risks="RSK-17", protocol="OQ-STA-03"),
    Row("URS-071", "FS-071-1", "statistics", G, level="unit", risks="RSK-17", protocol="OQ-STA-04",
        notes="not implemented: statistics output does not record library versions, seed and input-table hash",
        proposed="test_stats_output_records_versions_seed_and_table_hash"),
    Row("URS-072", "FS-072-1", "statistics", V, [D + "test_services.py::test_results_rows"],
        level="integration", risks="RSK-16", protocol="OQ-STA-02"),
    Row("URS-072", "FS-072-2", "statistics", G, level="integration", risks="RSK-16", protocol="OQ-STA-02",
        notes="not implemented: no exclusion-with-reason workflow", proposed="test_exclusion_requires_reason_and_is_listed_in_report"),
    Row("URS-075", "FS-075-1", "blinding", V, ["tests/test_api.py::test_blinding",
                                                "tests/test_store_api_workflows.py::test_blinded_specimen_listing_and_export"],
        level="integration", risks="RSK-12", protocol="OQ-BLD-01"),
    Row("URS-075", "FS-075-3", "blinding", V, [D + "test_main_window.py::test_blinded_mode_and_audit_verify",
                                                D + "test_services.py::test_results_rows",
                                                D + "test_review_fixes.py::test_ux09_blinded_mode_hides_identity_everywhere",
                                                TG + "test_blinded_mode_switch_records_ui_blinded_mode_event"],
        level="system", risks="RSK-12", protocol="OQ-BLD-02",
        notes="group name, animal ID and file name hidden in the tree, the Results rows and the viewer info bar for "
              "each of the five roles and shown again when switched off; every switch audited ui.blinded_mode "
              "{on: true/false} under the signed-in user"),
    Row("URS-075", "FS-075-4", "blinding", V, ["tests/test_security_fixes.py::test_S06_unblinded_report_download_denied",
                                                D + "test_cycle2_fixes.py::test_c2_03_study_blinding_enforced_for_reviewer",
                                                D + "test_review_fixes.py::test_ux09_blinded_mode_hides_identity_everywhere",
                                                TG + "test_blinded_download_denial_is_audited"],
        level="integration", risks="RSK-12", protocol="OQ-BLD-03",
        notes="report generated with unblinded allocation is marked (reports.unblinded=1; blinded reports 0); its "
              "export, and that of an identifying report of a now-blinded study, is refused to a reviewer with no file "
              "written and audited report.blinded_download_denied (report id, user); allowed to a user with unblind"),
    Row("URS-075", "FS-075-2", "blinding", V, ["tests/test_api.py::test_blinding",
                                                D + "test_cycle2_fixes.py::test_c2_03_study_blinding_enforced_for_reviewer",
                                                TG + "test_desktop_unblind_requires_reason"],
        level="integration", risks="RSK-12", protocol="OQ-BLD-04",
        notes="desktop unblind_study: refused without unblind permission, with a wrong password and with a missing or "
              "short (< 5 characters) reason (service and Unblind dialog; nothing audited); Study > Unblind study enabled "
              "for the study director and unblinds from the window; audited study.unblind with signer and reason"),
    Row("URS-076", "FS-076-1", "blinding", G, level="integration", risks="RSK-12", protocol="OQ-BLD-04",
        notes="not implemented", proposed="test_post_unblinding_edits_flagged_in_report"),
    # ------------------------------------------------------------------ 3.9 reporting
    Row("URS-080", "FS-080-1", "reporting", V, [D + "test_services.py::test_report_with_watermark_and_preview",
                                                 "tests/test_analysis_modules.py::test_build_pdf_and_figures",
                                                 "tests/test_report_bounds.py::test_pdf_banner_and_bounds",
                                                 "tests/test_report_bounds.py::test_report_prints_refused_values_as_not_measured_with_reasons",
                                                 TG + "test_report_provenance_section_complete"],
        level="integration", risks="RSK-18", protocol="OQ-REP-01",
        notes="banner, study, data class, software version, support-filtered specimen table, corrections table of a "
              "corrected segmentation, support section, reproducibility block (software version, git commit and the "
              "analysis configuration hashes, carried over on label revisions; added 2026-11-28) and sign-off table "
              "asserted in the desktop PDF; acquisition parameters are outside this FS item (CRO-06)"),
    Row("URS-081", "FS-081-1", "reporting", P, [D + "test_services.py::test_report_with_watermark_and_preview"],
        level="integration", risks="RSK-33", protocol="OQ-REP-02",
        notes="PDF + CSV export and report.export audit asserted; JSON provenance and label-map export not offered in the desktop",
        proposed="test_desktop_exports_json_provenance_and_label_maps"),
    Row("URS-082", "FS-082-1", "reporting", G, level="system", risks="RSK-18;RSK-28", protocol="OQ-REP-03",
        notes="not implemented", proposed="test_report_regeneration_matches_original_numerics"),
    Row("URS-083", "FS-083-2", "reporting", V, ["tests/test_analysis_modules.py::test_group_stats_comparisons_and_csv_injection"],
        risks="RSK-19", protocol="OQ-REP-04"),
    Row("URS-083", "FS-083-1", "reporting", G, level="unit", risks="RSK-19", protocol="OQ-REP-04",
        notes="locale independence and round-trip precision not tested",
        proposed="test_csv_locale_independent_full_precision_units_in_header"),
    # ------------------------------------------------------------------ 3.10 review and signatures
    Row("URS-090", "FS-090-1", "signature", P, ["tests/test_store_api_workflows.py::test_reviews_on_reports_and_unknown_objects",
                                                 "tests/test_security_fixes.py::test_S08_review_requires_existing_object"],
        risks="RSK-26", protocol="OQ-SIG-01",
        notes="decision values validated; there is no draft/in-review/approved state machine",
        proposed="test_review_state_machine_rejects_invalid_transitions"),
    Row("URS-091", "FS-091-1", "signature", V, [D + "test_services.py::test_review_requires_reauth_and_separation_of_duties",
                                                 "tests/test_store_api_workflows.py::test_reviews_on_reports_and_unknown_objects",
                                                 D + "test_review_fixes.py::test_ux07_08_report_signoff_roles_gates_and_signed_rows",
                                                 TG + "test_signature_meaning_rule_and_review_panel_history",
                                                 TGL + "test_api_refuses_signature_meaning_shorter_than_5"],
        level="integration", risks="RSK-26", protocol="OQ-SIG-02",
        notes="meaning < 5 characters refused by the desktop and the API before re-authentication (the Store itself "
              "does not check the length); review row stores reviewer, UTC time, decision, meaning and comment; the "
              "Review panel lists the history (time, reviewer, signature role, decision, meaning, comment on hover); "
              "the signed PDF copy shows the in-system signers, roles and meaning"),
    Row("URS-092", "FS-092-1", "signature", V, [D + "test_services.py::test_review_requires_reauth_and_separation_of_duties",
                                                 "tests/test_api.py::test_end_to_end"],
        level="integration", risks="RSK-26", protocol="OQ-SIG-02"),
    Row("URS-092", "FS-092-2", "signature", P, ["tests/test_security_gen2.py::test_reauthentication_counts_towards_lockout",
                                                 "tests/test_security_gen2.py::test_review_endpoint_cannot_bruteforce_password",
                                                 D + "test_admin_lock_audit.py::test_idle_lock_hides_project_and_unlock_uses_lockout",
                                                 D + "test_cycle2_fixes.py::test_c2_07_window_signs_out_deactivated_user"],
        level="integration", risks="RSK-23;RSK-26", protocol="OQ-SIG-03",
        notes="Project.reauthenticate now delegates to Store.reauthenticate (earlier bypass fixed); lockout and the "
              "inactive-account refusal asserted for the store, the API and desktop unlock; repeated failed desktop "
              "signatures (sign_review) locking the account is not asserted",
        proposed="test_desktop_reauth_failures_lock_account"),
    Row("URS-093", "FS-093-1", "signature", V, ["tests/test_store_api_workflows.py::test_reviews_on_reports_and_unknown_objects"],
        level="integration", risks="RSK-26;RSK-18", protocol="OQ-SIG-05",
        notes="signature row stores the SHA-256 of the signed labels or report"),
    Row("URS-093", "FS-093-2", "signature", G, level="integration", risks="RSK-26;RSK-18", protocol="OQ-SIG-05",
        notes="not implemented: no display of signatures invalidated by later changes",
        proposed="test_change_after_signature_shows_signature_superseded"),
    # ------------------------------------------------------------------ 3.11 audit trail
    Row("URS-100", "FS-100-1", "audit", V, ["tests/test_audit_properties.py::test_triggers_block_update_and_delete",
                                             "tests/test_api.py::test_audit_chain_detects_tampering"],
        risks="RSK-20", protocol="OQ-AUD-01"),
    Row("URS-100", "FS-100-2", "audit", V, [D + "test_import.py::test_run_assigns_and_logs_rejections",
                                             D + "test_services.py::test_label_revision_audit",
                                             D + "test_services.py::test_report_with_watermark_and_preview",
                                             D + "test_services.py::test_review_requires_reauth_and_separation_of_duties"],
        level="integration", risks="RSK-20", protocol="OQ-AUD-02"),
    Row("URS-101", "FS-101-1", "audit", P, ["tests/test_audit_properties.py::test_events_filtering_and_canonical_json",
                                             D + "test_services.py::test_label_revision_audit"],
        risks="RSK-20", protocol="OQ-AUD-02",
        notes="old/new values are not captured generally (hashes and deltas only for some actions)",
        proposed="test_audit_entries_carry_old_new_values_and_reason"),
    Row("URS-102", "FS-102-1", "audit", V, ["tests/test_audit_properties.py::test_any_single_field_tamper_is_detected",
                                             "tests/test_audit_properties.py::test_deleting_a_non_tail_row_is_detected",
                                             "tests/test_audit_properties.py::test_reordering_rows_is_detected",
                                             "tests/test_audit_properties.py::test_concurrent_writers_keep_one_chain",
                                             D + "test_main_window.py::test_blinded_mode_and_audit_verify"],
        risks="RSK-20", protocol="OQ-AUD-03"),
    Row("URS-102", "FS-102-2", "audit", V, ["tests/test_audit_properties.py::test_tail_truncation_needs_anchor",
                                             "tests/test_audit_properties.py::test_anchor_from_empty_log_verifies",
                                             "tests/test_security_fixes.py::test_S11_anchor_detects_truncation",
                                             D + "test_cycle3_fixes.py::test_report_prints_audit_anchor_and_anchor_file_is_written",
                                             D + "test_cycle3_fixes.py::test_rewritten_trail_disables_signatures"],
        risks="RSK-21", protocol="OQ-AUD-05",
        notes="desktop writes anchors automatically to a file outside the project folder and prints the chain head on "
              "reports; at sign-in a rewritten or truncated trail is detected (audit.anchor_mismatch) and signatures are "
              "refused; there is no manual import of an anchor held by a third party"),
    Row("URS-103", "FS-103-1", "audit", P, ["tests/test_audit_properties.py::test_triggers_block_update_and_delete"],
        risks="RSK-20", protocol="OQ-AUD-04",
        notes="SQL update/delete blocked; absence of any disabling setting not tested; OS users can drop triggers (RSK-48)",
        proposed="test_no_setting_or_code_path_disables_audit"),
    Row("URS-104", "FS-104-1", "audit", P, [D + "test_main_window.py::test_blinded_mode_and_audit_verify"],
        level="system", risks="RSK-20", protocol="OQ-AUD-07",
        notes="chain verification from the Audit tab asserted; filters and role restriction not asserted",
        proposed="test_audit_view_filters_and_role_restriction"),
    Row("URS-104", "FS-104-2", "audit", P, [D + "test_admin_lock_audit.py::test_audit_export_csv_json_with_verification",
                                             D + "test_admin_lock_audit.py::test_audit_export_reports_broken_chain",
                                             D + "test_cycle2_fixes.py::test_c2_14_16_blinded_outputs_and_verifiable_audit_export"],
        level="integration", risks="RSK-20", protocol="OQ-AUD-07",
        notes="whole-trail CSV/JSON export with chain-verification result (OK or BROKEN at event n), audited, role-"
              "restricted, re-verifiable rows; export of a filtered view and PDF export are not implemented",
        proposed="test_filtered_audit_export_with_verification_status"),
    Row("URS-105", "FS-105-1", "audit", V, ["tests/test_store_api_workflows.py::test_delete_study_data_removes_files_and_keeps_audit"],
        level="integration", risks="RSK-31", protocol="OQ-RET-02"),
    Row("URS-106", "FS-106-1", "audit", V, ["tests/test_controls.py::test_audit_timestamps_utc_monotonic",
                                             "tests/test_audit_properties.py::test_timestamp_is_one_instant"],
        risks="RSK-22", protocol="OQ-AUD-06"),
    Row("URS-106", "FS-106-2", "audit", G, level="procedure", risks="RSK-22", protocol="IQ-05",
        notes="workstation clock synchronisation is a user-organisation control; no in-application check",
        proposed="IQ-05 execution record"),
    # ------------------------------------------------------------------ 3.12 configuration, models, jobs
    Row("URS-110", "FS-110-1", "configuration", P, ["tests/test_analysis_modules.py::test_pipeline_analyze_end_to_end_and_manual_roi"],
        level="integration", risks="RSK-27", protocol="OQ-CFG-01",
        notes="config hash computed; the resolved configuration is not stored as a snapshot linked to the measurement",
        proposed="test_run_stores_resolved_config_snapshot_hash"),
    Row("URS-111", "FS-111-1", "models", V, ["tests/test_ml_phantom.py::test_load_model_verifies_hash_before_deserialising",
                                             "tests/test_ml_phantom.py::test_load_model_refuses_pickled_code_even_if_registered",
                                             "tests/test_controls.py::test_trained_model_roundtrips_through_safe_loading",
                                             "tests/test_ml_phantom.py::test_onnx_runtime_matches_torch_and_verifies_hash"],
        risks="RSK-10", protocol="OQ-MOD-01", notes="ONNX loader time-of-check/time-of-use issue open (QA-023)"),
    Row("URS-111", "FS-111-2", "models", V, ["tests/test_ml_phantom.py::test_pipeline_rf_requires_trusted_local_flag",
                                             "tests/test_security_fixes.py::test_S02_model_paths_and_pickles_rejected",
                                             TG + "test_desktop_refuses_pickled_rf_models"],
        level="integration", risks="RSK-10;RSK-45", protocol="OQ-MOD-01",
        notes="library trusted-local flag and API refusal tested; desktop analyze_scan refuses rf: models, also with "
              "the trusted-local flag set, before the analysis job starts (nothing stored)"),
    Row("URS-112", "FS-112-1", "models", G, level="integration", risks="RSK-10", protocol="OQ-MOD-02",
        notes="not implemented: no release status; the desktop lists every locked model with its licence tag",
        proposed="test_only_released_models_selectable"),
    Row("URS-113", "FS-113-1", "configuration", P, ["tests/test_stats_reference.py::test_bootstrap_ci_contains_mean_and_is_deterministic",
                                                     "tests/test_ml_phantom.py::test_domain_randomised_sampler_shapes_and_determinism"],
        evidence=["experiments/exp_P_reproducibility.py"], level="system", risks="RSK-28;RSK-29", protocol="OQ-CFG-02",
        notes="Experiment P shows bit-identical pipeline reruns; no rerun regression test in the suite",
        proposed="test_pipeline_rerun_bit_identical"),
    Row("URS-114", "FS-114-1", "jobs", V, [D + "test_jobs.py::test_job_done", D + "test_jobs.py::test_job_cancellation",
                                            D + "test_jobs.py::test_cancel_before_start", D + "test_jobs.py::test_error_capture",
                                            D + "test_jobs.py::test_ui_thread_not_blocked"],
        risks="RSK-46", protocol="OQ-JOB-01"),
    Row("URS-114", "FS-114-2", "jobs", V, [D + "test_jobs.py::test_analysis_job_records_in_store_and_cancels",
                                            "tests/test_api.py::test_job_cancel_and_recovery",
                                            "tests/test_store_api_workflows.py::test_job_runner_cancel_get_list_and_stale_privilege"],
        level="integration", risks="RSK-46", protocol="OQ-JOB-02"),
    # ------------------------------------------------------------------ 3.13 data management
    Row("URS-120", "FS-120-1", "data management", P, ["tests/test_api.py::test_backup_restores",
                                                       "tests/test_security_gen2.py::test_interrupted_backup_target"],
        level="integration", risks="RSK-30", protocol="OQ-BKP-01",
        notes="database backup only; scan stores, reports and licence not included; no desktop backup function",
        proposed="test_project_backup_includes_db_scans_reports_with_manifest"),
    Row("URS-121", "FS-121-1", "data management", P, ["tests/test_api.py::test_backup_restores",
                                                       "tests/test_security_gen2.py::test_reopen_is_idempotent_and_chain_survives"],
        level="integration", risks="RSK-30", protocol="OQ-BKP-02",
        notes="restored database chain verifies; no whole-project restore verification", proposed="test_project_restore_verifies_hashes_and_chain"),
    Row("URS-122", "FS-122-1", "data management", G, level="integration", risks="RSK-31", protocol="OQ-RET-01",
        notes="not implemented: orgs.retention_days is stored but not enforced", proposed="test_delete_blocked_during_retention"),
    Row("URS-123", "FS-123-1", "data management", P, ["tests/test_store_api_workflows.py::test_delete_study_data_removes_files_and_keeps_audit"],
        level="integration", risks="RSK-31", protocol="OQ-RET-02",
        notes="permission, reason and audit tested; no second approval, legal hold or retention check",
        proposed="test_deletion_dual_approval_and_legal_hold"),
    Row("URS-124", "FS-124-1", "data management", P, ["tests/test_store_api_workflows.py::test_blinded_specimen_listing_and_export"],
        level="integration", risks="RSK-33", protocol="OQ-ARC-01",
        notes="export_study returns JSON (records + audit); no files, no manifest, not offered in the desktop",
        proposed="test_study_archive_export_manifest_verifies"),
    Row("URS-125", "FS-125-1", "data management", V, ["tests/test_security_gen2.py::test_corrupted_database_file_fails_clearly",
                                                       "tests/test_security_gen2.py::test_truncated_database_fails_or_detects",
                                                       "tests/test_security_gen2.py::test_reopen_is_idempotent_and_chain_survives",
                                                       "tests/test_security_gen2.py::test_read_only_database_file_rejects_writes"],
        level="integration", risks="RSK-32", protocol="OQ-DB-01"),
    Row("URS-125", "FS-125-2", "data management", G, level="system", risks="RSK-32", protocol="OQ-DB-02",
        notes="not implemented: a project opened by two application instances is not detected",
        proposed="test_second_instance_opening_project_is_warned_or_read_only"),
    # ------------------------------------------------------------------ 3.14 security
    Row("URS-131", "FS-131-1", "security", P, [D + "test_main_window.py::test_about_lists_third_party_licences"],
        evidence=["docs/security/pip_audit_output.txt", "docs/security/SBOM.csv"],
        level="static", risks="RSK-29", protocol="IQ-02",
        notes="About component/licence list asserted; manual pip-audit and SBOM; dependency floors allow vulnerable "
              "versions (QA-024); no hash-pinned lock file",
        proposed="ci_pip_audit_on_hash_pinned_lock_file"),
    Row("URS-132", "FS-132-1", "security", V, ["tests/test_security_gen2.py::test_reauthentication_counts_towards_lockout",
                                                D + "test_services.py::test_review_requires_reauth_and_separation_of_duties",
                                                "tests/test_controls.py::test_author_cannot_approve_own_segmentation",
                                                D + "test_admin_lock_audit.py::test_user_admin_add_deactivate_reset_audited",
                                                D + "test_cycle2_fixes.py::test_c2_09_role_change_audited_and_database_edit_detected",
                                                D + "test_services.py::test_report_with_watermark_and_preview",
                                                TG + "test_security_events_logged",
                                                TG + "test_blinded_download_denial_is_audited"],
        level="integration", risks="RSK-23", protocol="OQ-ACC-08",
        notes="every listed event asserted: auth.login and auth.login_failed (bad password, unknown user) at desktop "
              "sign-in, authz.denied for desktop actions (unblind, write, audit export), auth.reauth_failed, "
              "review.reauth_failed, review.self_approval_denied, user.*, report.export, report.blinded_download_denied"),
    Row("URS-133", "FS-133-1", "security", V, ["tests/test_io_destructive.py::test_zarr_pickle_codec_rejected_before_decoding",
                                                "tests/test_io_destructive.py::test_huge_nifti_dims_fail_fast",
                                                "tests/test_io_destructive.py::test_huge_zarr_shape_fail_fast",
                                                "tests/test_io_destructive.py::test_ome_tiff_external_reference_rejected",
                                                "tests/test_io_destructive.py::test_symlinks_rejected_in_uploads",
                                                "tests/test_safe_archive.py::test_zip_path_traversal_rejected",
                                                "tests/test_safe_archive.py::test_zip_many_small_members_aggregate_ratio",
                                                "tests/test_ml_phantom.py::test_load_model_refuses_pickled_code_even_if_registered"],
        risks="RSK-45", protocol="OQ-SEC-01",
        notes="library safe-input checks; desktop import of local files has not been reviewed for use of safe mode"),
    # ------------------------------------------------------------------ 3.15 documentation
    Row("URS-140", "FS-140-1", "documentation", P, [], evidence=["docs/desktop/USER_GUIDE.md"], level="document review",
        risks="RSK-35", protocol="OQ-DOC-01", notes="user guide exists; completeness review not performed",
        proposed="OQ-DOC-01 review record"),
    Row("URS-141", "FS-141-1", "documentation", G, level="document review", risks="RSK-29", protocol="OQ-DOC-02",
        notes="docs/user/RELEASE_NOTES_GEN2.md exists but follows no template (no change IDs, no verification-evidence "
              "reference); OQ-DOC-02 not executed", proposed="OQ-DOC-02 review record"),
    # ------------------------------------------------------------------ 3.16 measurement support / abstention
    Row("URS-150", "FS-150-1", "measurement support", V, ["tests/test_advisor.py::test_dense_ha_low_noise_supported",
                                                           "tests/test_advisor.py::test_supported_set_shrinks_with_noise",
                                                           "tests/test_advisor.py::test_assessment_records_version",
                                                           "tests/test_advisor.py::test_pipeline_reports_support",
                                                           "tests/test_advisor.py::test_oracle_is_upper_bound_for_threshold_rules"],
        evidence=["docs/science/MEASUREMENT_SUPPORT.md"], risks="RSK-37", protocol="OQ-SUP-01",
        notes="policy thresholds checked only in simulation (S1/S1b; STAT-04 accepted limitation)"),
    Row("URS-150", "FS-150-2", "measurement support", V, ["tests/test_advisor.py::test_metals_refused",
                                                           "tests/test_advisor.py::test_bone_derived_never_intensity_supported",
                                                           "tests/test_advisor.py::test_dbm_new_bone_not_supported",
                                                           "tests/test_advisor.py::test_radiolucent_graft_not_visible",
                                                           "tests/test_advisor.py::test_no_graft_design",
                                                           "tests/test_advisor.py::test_scarce_graft_refuses_graft_volume_only",
                                                           "tests/test_advisor.py::test_support_requires_robustness_to_low_graft_share"],
        risks="RSK-37", protocol="OQ-SUP-02"),
    Row("URS-151", "FS-151-1", "measurement support", V, ["tests/test_advisor.py::test_apply_support_suppresses_unsupported",
                                                           "tests/test_advisor.py::test_pipeline_reports_support",
                                                           D + "test_services.py::test_measurement_support_statuses"],
        level="integration", risks="RSK-37", protocol="OQ-SUP-03"),
    Row("URS-151", "FS-151-2", "measurement support", V, [D + "test_services.py::test_label_revision_audit"],
        level="integration", risks="RSK-37", protocol="OQ-SUP-03"),
    Row("URS-152", "FS-152-1", "measurement support", V, [D + "test_services.py::test_measurement_support_statuses",
                                                           D + "test_services.py::test_results_rows",
                                                           D + "test_review_fixes.py::test_ux03_results_csv_and_report_have_no_number_for_not_supported",
                                                           D + "test_review_fixes.py::test_ux02_accept_roi_is_signed_audited_and_clears_flag",
                                                           TG + "test_results_csv_contains_support_columns"],
        level="integration", risks="RSK-38", protocol="OQ-SUP-04",
        notes="Results-tab Support column shows supported, flagged, not supported and not analysed; a not-supported "
              "value reads 'not measured' with the status and reason as tooltip; the results CSV has a support and a "
              "reasons column per endpoint and no number for not-supported values"),
    Row("URS-152", "FS-152-2", "measurement support", P, ["tests/test_report_bounds.py::test_report_prints_refused_values_as_not_measured_with_reasons",
                                                           "tests/test_report_bounds.py::test_renderer_enforces_refusal_in_group_stats_and_csv",
                                                           D + "test_cycle3_fixes.py::test_stale_and_unbound_records_show_not_assessed_in_report"],
        level="integration", risks="RSK-38", protocol="OQ-SUP-04",
        notes="PDF: refused values never printed as numbers, 'n/m', support section with reason, conditions and advisor "
              "version; CSV <endpoint>__support columns asserted; the '(c)' mark on conditional values is not asserted "
              "(the string also occurs in the legend)",
        proposed="test_conditional_values_marked_c_in_specimen_table"),
    Row("URS-153", "FS-153-1", "measurement support", V, ["tests/test_advisor.py::test_unknown_material_refused",
                                                           "tests/test_advisor.py::test_measured_samples_override_unknown_material",
                                                           "tests/test_advisor.py::test_small_reference_samples_ignored_and_bone_rule_not_bypassed",
                                                           "tests/test_advisor.py::test_pipeline_reports_support"],
        risks="RSK-37", protocol="OQ-SUP-05"),
    # ------------------------------------------------------------------ 3.17 validation records
    Row("URS-160", "FS-160-1", "validation records", V, ["tests/test_advisor.py::test_validation_records_synthetic_never_qualifies"],
        risks="RSK-39", protocol="OQ-VAL-01"),
    Row("URS-160", "FS-160-2", "validation records", P, ["tests/test_advisor.py::test_validation_records_hostile_key_id_and_corrupt_file"],
        level="integration", risks="RSK-39", protocol="OQ-VAL-02",
        notes="validated_for outcomes and the support binding on the stored validation_ok boolean asserted; no test runs "
              "the pipeline and asserts that it calls validated_for and stores segmentation.validation_record",
        proposed="test_pipeline_uses_validation_record_and_records_reason"),
    Row("URS-161", "FS-161-1", "validation records", P, ["tests/test_advisor.py::test_validation_records_tamper_detected",
                                                          "tests/test_advisor.py::test_validation_records_synthetic_never_qualifies",
                                                          "tests/test_advisor.py::test_validation_records_hostile_key_id_and_corrupt_file"],
        level="unit", risks="RSK-39", protocol="OQ-VAL-03",
        notes="validation_records.json is an Ed25519-signed envelope: edited payload, untrusted or test signer and corrupt "
              "file are refused; content hash in the model registry and audited, approved additions (SOP-007) not tested",
        proposed="test_validation_record_store_change_detected"),
    # ------------------------------------------------------------------ 3.18 material characterisation
    Row("URS-170", "FS-170-1", "material characterisation", V, ["tests/test_advisor.py::test_characterise_material_and_use_in_advisor",
                                                                 "tests/test_advisor.py::test_characterise_from_day0_recovers_graft_level"],
        risks="RSK-40", protocol="OQ-MAT-01"),
    Row("URS-170", "FS-170-2", "material characterisation", V, ["tests/test_advisor.py::test_characterise_rejects_tiny_mask",
                                                                 "tests/test_advisor.py::test_small_reference_samples_ignored_and_bone_rule_not_bypassed"],
        risks="RSK-40", protocol="OQ-MAT-01"),
    Row("URS-171", "FS-171-1", "material characterisation", V, ["tests/test_advisor.py::test_characterise_material_and_use_in_advisor",
                                                                 "tests/test_advisor.py::test_characterisation_is_bound_to_its_acquisition",
                                                                 TGL + "test_characterisation_incompatible_filter_refused"],
        risks="RSK-40", protocol="OQ-MAT-02",
        notes="voxel size (25 % boundary on both sides), kVp, filter and scanner-model refusals asserted; a field "
              "missing from either acquisition record is not compared (reuse allowed)"),
    Row("URS-171", "FS-171-2", "material characterisation", G, level="system", risks="RSK-40", protocol="OQ-MAT-03",
        notes="not implemented: no desktop workflow to run, store and attach a characterisation",
        proposed="test_desktop_characterisation_stored_attached_and_audited"),
    # ------------------------------------------------------------------ 3.19 longitudinal QC
    Row("URS-180", "FS-180-1", "longitudinal QC", V, ["tests/test_longitudinal_v2.py::test_registration_qc_passes_aligned_and_flags_shift",
                                                       "tests/test_longitudinal_v2.py::test_registration_qc_exact_tolerance_shift_passes",
                                                       "tests/test_analysis_modules.py::test_rigid_registration_recovers_known_motion"],
        risks="RSK-41", protocol="OQ-LON-01", notes="synthetic data only"),
    Row("URS-180", "FS-180-2", "longitudinal QC", G, level="system", risks="RSK-41", protocol="OQ-LON-04",
        notes="not implemented: longitudinal functions are library-only, not in the desktop",
        proposed="test_desktop_longitudinal_pairing_registration_qc_and_audit"),
    Row("URS-181", "FS-181-1", "longitudinal QC", V, ["tests/test_advisor.py::test_day0_conditions_and_displacement_limit"],
        risks="RSK-41", protocol="OQ-LON-02"),
    Row("URS-181", "FS-181-2", "longitudinal QC", V, ["tests/test_longitudinal_v2.py::test_track_granules_recovers_known_shift",
                                                       "tests/test_longitudinal_v2.py::test_track_granules_reports_untracked_when_graft_disappears",
                                                       "tests/test_analysis_modules.py::test_day0_propagation_change_map_and_volumes"],
        risks="RSK-41", protocol="OQ-LON-02", notes="synthetic data only"),
    Row("URS-182", "FS-182-1", "longitudinal QC", V, ["tests/test_longitudinal_v2.py::test_propagate_roi_after_motion"],
        evidence=["experiments/results/exp_F2_roi_propagation.json"], risks="RSK-41;RSK-07", protocol="OQ-LON-03",
        notes="synthetic data only"),
    # ------------------------------------------------------------------ 3.20 licence verification
    Row("URS-190", "FS-190-1", "licence", V, [D + "test_licensing.py::test_valid", D + "test_licensing.py::test_tampered_payload",
                                               D + "test_licensing.py::test_tampered_expiry_whitespace_and_signature",
                                               D + "test_licensing.py::test_wrong_key", D + "test_licensing.py::test_malformed_inputs",
                                               D + "test_licensing.py::test_sign_rejects_bad_payload"],
        risks="RSK-42", protocol="OQ-LIC-01"),
    Row("URS-190", "FS-190-2", "licence", V, [D + "test_licensing.py::test_expired", D + "test_licensing.py::test_perpetual",
                                               D + "test_licensing.py::test_machine_binding"],
        risks="RSK-42", protocol="OQ-LIC-02"),
    Row("URS-191", "FS-191-1", "licence", V, [D + "test_services.py::test_report_with_watermark_and_preview",
                                               D + "test_licensing.py::test_expired",
                                               D + "test_licensing.py::test_test_key_only_when_allowed",
                                               D + "test_main_window.py::test_selftest_entry_point"],
        level="integration", risks="RSK-42", protocol="OQ-LIC-03"),
    Row("URS-192", "FS-192-1", "licence", V, [D + "test_licensing.py::test_test_key_only_when_allowed",
                                               D + "test_licensing.py::test_no_production_key_shipped",
                                               D + "test_licensing.py::test_tool_keygen_and_install"],
        risks="RSK-42", protocol="OQ-LIC-04"),
    # ------------------------------------------------------------------ 3.21 workflow timing
    Row("URS-200", "FS-200-1", "workflow timing", V, [D + "test_services.py::test_workflow_timing"],
        level="integration", risks="RSK-43", protocol="OQ-TIM-01"),
    Row("URS-200", "FS-200-2", "workflow timing", P, [D + "test_services.py::test_workflow_timing"],
        level="integration", risks="RSK-43", protocol="OQ-TIM-01",
        notes="enable/disable and export are audited in code; the test does not assert the audit events",
        proposed="test_timing_enable_disable_export_audited"),
    Row("URS-201", "FS-201-1", "workflow timing", P, [D + "test_services.py::test_workflow_timing"],
        level="integration", risks="RSK-43;RSK-44", protocol="OQ-TIM-02",
        notes="local storage asserted; non-transmission covered only by FS-211-1 (GAP)",
        proposed="test_no_socket_connections_during_selftest"),
    Row("URS-202", "FS-202-1", "workflow timing", V, [D + "test_services.py::test_workflow_timing"],
        level="integration", risks="RSK-43", protocol="OQ-TIM-03"),
    # ------------------------------------------------------------------ 3.22 offline operation
    Row("URS-210", "FS-210-1", "offline", P, [D + "test_main_window.py::test_selftest_entry_point"],
        level="system", risks="RSK-44", protocol="OQ-OFF-01",
        notes="self-test runs the whole workflow headless, but network availability is not controlled during the test",
        proposed="test_selftest_passes_with_network_blocked"),
    Row("URS-211", "FS-211-1", "offline", G, level="system", risks="RSK-44", protocol="OQ-OFF-02",
        notes="static review found no networking code in osteoquant/; no test", proposed="test_no_socket_connections_during_selftest"),
]


# ============================================================================ checks
def collect_tests() -> set[str]:
    r = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider"],
                       cwd=ROOT, capture_output=True, text=True, timeout=900)
    ids = set()
    for line in r.stdout.splitlines():
        line = line.strip()
        if "::" not in line or line.startswith(("=", "-")):
            continue
        parts = line.split("::")
        ids.add(parts[0] + "::" + re.sub(r"\[.*\]$", "", parts[-1]))
    if not ids:
        raise SystemExit("pytest collection returned no tests:\n" + r.stdout[-2000:] + r.stderr[-2000:])
    return ids


def doc_ids(path: Path, prefix: str) -> set[str]:
    pat = re.compile(r"^\|\s*(" + prefix + r"-[0-9]{3}(?:-[0-9]+)?)\s*\|")
    return {m.group(1) for line in path.read_text(encoding="utf-8").splitlines() if (m := pat.match(line))}


def check(rows: list[Row], collected: set[str] | None) -> list[str]:
    errors = []
    seen = set()
    for r in rows:
        key = r.fs
        if key in seen:
            errors.append(f"{key}: duplicate FS row")
        seen.add(key)
        if not r.fs.startswith("FS-" + r.urs[4:] + "-"):
            errors.append(f"{r.fs}: FS id does not belong to {r.urs}")
        if r.status not in (V, P, G):
            errors.append(f"{r.fs}: unknown status {r.status}")
        if r.status == V and not r.tests:
            errors.append(f"{r.fs}: VERIFIED without a test")
        if r.status == P and not (r.tests or r.evidence):
            errors.append(f"{r.fs}: PARTIAL without a test or evidence")
        if r.status == G and r.tests:
            errors.append(f"{r.fs}: GAP but tests are listed")
        if r.status in (P, G) and not r.proposed:
            errors.append(f"{r.fs}: {r.status} without a proposed test/review")
        for t in r.tests:
            if not (ROOT / t.split("::")[0]).is_file():
                errors.append(f"{r.fs}: test file missing: {t}")
            elif collected is not None and t not in collected:
                errors.append(f"{r.fs}: test not collected by pytest: {t}")
        for e in r.evidence:
            if not (ROOT / e).exists():
                errors.append(f"{r.fs}: evidence file missing: {e}")
        if r.urs in RETIRED_URS:
            errors.append(f"{r.fs}: maps a retired requirement {r.urs}")
    urs_doc = doc_ids(QDIR / "URS.md", "URS") - RETIRED_URS
    fs_doc = doc_ids(QDIR / "FUNCTIONAL_SPEC.md", "FS") - RETIRED_FS
    urs_map = {r.urs for r in rows}
    fs_map = {r.fs for r in rows}
    for x in sorted(urs_doc - urs_map):
        errors.append(f"{x}: in URS.md but not mapped")
    for x in sorted(urs_map - urs_doc):
        errors.append(f"{x}: mapped but not in URS.md")
    for x in sorted(fs_doc - fs_map):
        errors.append(f"{x}: in FUNCTIONAL_SPEC.md but not mapped")
    for x in sorted(fs_map - fs_doc):
        errors.append(f"{x}: mapped but not in FUNCTIONAL_SPEC.md")
    proto = (QDIR / "IQ_PROTOCOL.md").read_text(encoding="utf-8") + (QDIR / "OQ_PROTOCOL.md").read_text(encoding="utf-8")
    for r in rows:
        for p in r.protocol.split(";"):
            if p and not re.search(r"\|\s*" + re.escape(p) + r"\s*\|", proto):
                errors.append(f"{r.fs}: protocol step {p} not found in IQ/OQ protocol")
    return errors


def render(rows: list[Row]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(COLUMNS)
    for r in rows:
        w.writerow([r.urs, r.fs, r.area, r.status, "; ".join(r.tests), "; ".join(r.evidence), r.level, r.risks,
                    r.protocol, r.notes, r.proposed])
    return buf.getvalue()


def counts_from_csv(text: str) -> collections.Counter:
    rows = list(csv.DictReader(io.StringIO(text)))
    return collections.Counter((x.get("status") or "").strip() for x in rows)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="check only; fail if the CSV on disk is out of date")
    ap.add_argument("--no-collect", action="store_true", help="skip pytest collection")
    a = ap.parse_args(argv)
    collected = None if a.no_collect else collect_tests()
    errors = check(ROWS, collected)
    for e in errors:
        print("ERROR", e)
    new = render(ROWS)
    old = CSV_PATH.read_text(encoding="utf-8") if CSV_PATH.exists() else ""
    before, after = counts_from_csv(old), counts_from_csv(new)
    n_tests = len({t for r in ROWS for t in r.tests})
    print(f"requirements: {len({r.urs for r in ROWS})} active URS, {len(RETIRED_URS)} retired; {len(ROWS)} FS rows; "
          f"{n_tests} distinct tests referenced" + ("" if collected is None else f" (of {len(collected)} collected)"))
    print("matrix on disk : " + ", ".join(f"{k} {before.get(k, 0)}" for k in (V, P, G)) + f" (rows {sum(before.values())})")
    print("matrix built   : " + ", ".join(f"{k} {after.get(k, 0)}" for k in (V, P, G)) + f" (rows {sum(after.values())})")
    by_urs = collections.defaultdict(set)
    for r in ROWS:
        by_urs[r.urs].add(r.status)
    urs_status = collections.Counter(V if s == {V} else G if s == {G} else P for s in by_urs.values())
    print("per URS (all FS rows VERIFIED / any mix / all GAP): " + ", ".join(f"{k} {urs_status.get(k, 0)}" for k in (V, P, G)))
    by_area = collections.defaultdict(collections.Counter)
    for r in ROWS:
        by_area[r.area][r.status] += 1
    print("per area (VERIFIED/PARTIAL/GAP): " + "; ".join(f"{k} {v[V]}/{v[P]}/{v[G]}" for k, v in by_area.items()))
    if errors:
        return 1
    if a.check:
        if old != new:
            print("ERROR traceability_matrix.csv is out of date; run scripts/build_traceability.py")
            return 1
        return 0
    CSV_PATH.write_text(new, encoding="utf-8")
    print(f"wrote {CSV_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
