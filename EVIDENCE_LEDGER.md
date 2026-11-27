# Evidence Ledger (Generation 2)

Every statement in customer-, investor- or grant-facing material must map to a row here or in the Generation-1
ledger `SCIENTIFIC_EVIDENCE.md` (rows 1–7, R1–R12, which remain valid with the caveats recorded there).

## Evidence classes
| Class | Meaning | May be stated as |
|---|---|---|
| E1 VERIFIED-SOURCE | Fact checked against a primary source this project fetched | fact, with citation |
| E2 PUBLISHED | Peer-reviewed finding by others | "X et al. reported…" |
| E3 REAL-RESULT | Result computed by this project on real public data | result with n, CI, dataset |
| E4 SYN-RESULT | Result on synthetic phantoms | "in simulation…" only |
| E5 CLAIM | Vendor/company claim | "X states…" |
| E6 ASSUMPTION | Parameter chosen without measurement | assumption, never as a result |
| E7 HYPOTHESIS | Commercial or scientific hypothesis under test | hypothesis |
| E8 UNKNOWN | Not known | say unknown |

## Generation-2 entries
| ID | Statement | Class | Source / evidence |
|---|---|---|---|
| G2-001 | The Gen-0 product UI required a local server and a browser | E3 (code fact) | FORENSIC_AUDIT FA-13 |
| G2-002 | "≈78% analyst time saving" is an assumption-derived model output, not a measurement | E6 | FORENSIC_AUDIT FA-06; exp_K_M effort_model |
| G2-003 | Synthetic-trained U-Net zero-shot on real dog micro-CT: Dice 0.379 | E3 | exp_H_I_real.json (n=5 test) |

(Entries are appended as Generation-2 experiments complete.)
