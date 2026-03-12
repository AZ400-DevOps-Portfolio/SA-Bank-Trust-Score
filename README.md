# 🏦 SA Bank Trust Score

> A data-driven consumer protection tool for South African banking customers.

Built by **Lindiwe Songelwa** | [LinkedIn](https://www.linkedin.com/in/lindiwe-songelwa) | [Portfolio](https://lindiwe-22.github.io/Portfolio-Website/)

---

## Why This Project Exists

South African consumers choose banks based on marketing — not evidence. This project changes that.

Using verified data from official regulatory bodies, this project builds a transparent **Trust Score** for each of South Africa's major retail banks — giving consumers, journalists, and researchers a data-driven basis for one of their most important financial decisions.

---

## Banks Covered

Standard Bank · FNB · Absa · Nedbank · Capitec · TymeBank

---

## Trust Score Dimensions

| Dimension | Weight | Source |
|---|---|---|
| Complaint resolution rate | 30% | OBS Annual Report 2023 |
| Consumer favour rate | 25% | OBS 2023 + NFO 2024 |
| Regulatory sanctions | 25% | SARB Prudential Authority 2022–2025 |
| Consumer sentiment | 20% | DataEQ 2024 + Sagaci Research 2025 |

---

## Project Phases

| Phase | Description | Status |
|---|---|---|
| **Phase 1** | Data science notebook — scoring model and visualisations | ✅ Complete |
| **Phase 2** | Streamlit dashboard — interactive consumer-facing web app | 🔜 Planned |
| **Phase 3** | DevOps pipeline — automated data updates and deployment | 🔜 Planned |

---

## Repository Structure
```
SA-Bank-Trust-Score/
├── data/
│   ├── complaints.csv        # OBS formal complaint statistics
│   ├── sanctions.csv         # SARB regulatory penalties
│   └── sentiment.csv         # DataEQ + Sagaci sentiment scores
├── notebooks/
│   └── bank_trust_score.ipynb
├── requirements.txt
└── README.md
```

---

## Run Locally
```bash
git clone https://github.com/Lindiwe-22/SA-Bank-Trust-Score.git
cd SA-Bank-Trust-Score
pip install -r requirements.txt
jupyter notebook notebooks/bank_trust_score.ipynb
```

---

## Data Sources

All data is publicly available from official sources:

- [OBS Annual Report 2023](https://nfosa.co.za)
- [NFO Annual Report 2024](https://nfosa.co.za)
- [SARB Prudential Authority Sanctions](https://www.resbank.co.za)
- [DataEQ SA Banking Index 2024](https://dataeq.com)
- [Sagaci Research 2025](https://sagaciresearch.com)

---

*© 2026 Lindiwe Songelwa. For educational and consumer advocacy purposes.*