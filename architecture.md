# Space Mission Assistant — Architecture

**Purpose:** A practice project to learn ML, Deep Learning, RAG, Agents, and Automation freely — before applying the same skills under pressure on the graduation project (AI-Powered Campus Management Platform). Mistakes here are cheap; that's the point.

---

## 1. System Overview

The assistant monitors a (simulated or real) space mission and:
1. Predicts the likelihood of mission/device failure from sensor data (ML)
2. Analyzes satellite images or sensor streams for anomalies (DL)
3. Answers questions about mission/vehicle documentation (RAG)
4. Decides what to do about a detected issue — alert, report, recheck (Agent)
5. Runs all of the above without manual triggering (Automation)

```
Sensor/Image Data ─┐
                    ├─► ML Model ────┐
                    ├─► DL Model ────┤
                    │                ├─► Agent ──► Action (alert / report / recheck)
Mission Docs ───────┴─► RAG System ──┘
                                        ▲
                                        │
                              Automation Layer (schedules/triggers everything above)
```

---

## 2. Components

### 2.1 ML — Failure Prediction
- **Input:** sensor telemetry (temperature, pressure, voltage, vibration, etc.)
- **Output:** probability of failure/malfunction
- **Approach:** classifier (start simple — logistic regression or random forest as baseline, then a small neural net if time allows)
- **Data:** open NASA telemetry/anomaly datasets, or simulated data if nothing suitable is found

### 2.2 DL — Image/Sensor Analysis
- **Input:** satellite images or sensor-stream-as-image data
- **Output:** anomaly flag/classification
- **Approach:** CNN, transfer learning from a pretrained vision model (don't train from scratch)
- **Status:** stretch goal — build the ML + RAG + Agent + Automation loop fully working first

### 2.3 RAG — Mission Documentation Q&A
- **Input:** mission/vehicle manuals (PDF)
- **Pipeline:** PDF → chunk → embed (multilingual-e5 or similar) → vector store → retrieve → LLM answers using retrieved context
- **Output:** answers to questions like "what's the safe operating temperature for component X?"

### 2.4 Agent — Decision Layer
- **Input:** ML prediction + DL anomaly flag + relevant RAG context
- **Decides:** inform engineer / generate report / run additional check / do nothing
- **Approach:** LLM with a tool-calling setup — each decision option is a callable tool (send_alert, generate_report, trigger_recheck)

### 2.5 Automation — Orchestration
- Chains steps 2.1–2.4 to run on a schedule or on new-data-arrival, with no manual trigger
- Simplest version: a scheduled script/cron job; more advanced: event-driven (new sensor reading → pipeline runs)

---

## 3. Tech Stack

| Layer | Tool |
|---|---|
| ML | scikit-learn / PyTorch |
| DL | PyTorch + pretrained CNN (transfer learning) |
| RAG | LangChain or plain retrieval + multilingual embedding model |
| Agent | LLM API (tool-calling) |
| API | FastAPI |
| Automation | Python scheduler / cron |
| Containerization | Docker |

---

## 4. Suggested Folder Structure

```
space-mission-assistant/
├── data/                 # raw + processed sensor/image/doc data
├── models/
│   ├── ml_failure/        # failure-prediction model + training script
│   └── dl_anomaly/        # image/sensor anomaly model
├── rag/
│   ├── ingest.py          # PDF → chunks → embeddings
│   └── retrieve.py
├── agent/
│   └── decision_agent.py
├── automation/
│   └── scheduler.py
├── api/
│   └── main.py             # FastAPI app tying it together
├── notebooks/               # experiments, freely messy
├── requirements.txt
└── README.md
```

---

## 5. Build Order

1. Small/simulated dataset first — don't wait for the perfect one
2. ML failure-prediction model — get this working end-to-end first
3. RAG over mission docs — reuse this pattern later for the Study Companion
4. Agent layer — LLM decides the action given ML + RAG context
5. Automation — chain it all to run unattended
6. DL image analysis — stretch goal, only after 1–5 work

---

## 6. Open Questions / To Decide Later
- Which dataset to use for step 1 (real NASA data vs. simulated)
- Which LLM API for the Agent and RAG generation
- Whether DL component is in scope given time constraints
