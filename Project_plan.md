# Project 15: Distributed Text Mining and Sentiment Analysis (Variant B)

Use MapReduce to analyze a large corpus of text for word frequency and sentiment insights. Classify sentiment using a pre‑trained lexicon (positive/negative/neutral).

---

## 1. Project Overview

- **Objective:**  
  1. Compute word frequencies over a large text corpus (tweets, reviews, headlines)  
  2. Classify each document’s sentiment (positive/negative/neutral) using a pre‑trained lexicon  
- **Deliverable:**  
  - Command‑line tool that ingest raw text, run MapReduce jobs, and print aggregate word counts and sentiment summaries  

## 2. Team Members 

- Stepan Vagin (lead)  
- Lana Ermolaeva      
- Savva Ponomarev    
- Vyacheslav Molchanov
- Danil Valiev        

## 3. Team Roles (5 Engineers)

| Engineer | Primary Focus                                                                 |
|:--------:|-------------------------------------------------------------------------------|
| E1       | Environment & Infrastructure (Hadoop/HDFS or local‑cluster setup)             |
| E2       | Data Ingestion & Preprocessing (reading, cleaning, partitioning)              |
| E3       | MapReduce WordCount Implementation                                            |
| E4       | Sentiment Classification Integration (lexicon lookup, neutral handling)       |
| E5       | Testing, Validation & Documentation (unit tests, end‑to‑end scripts, README)  |

## 3. Timeline & Milestones

| Day     | Milestone                                                  |
|:-------:|------------------------------------------------------------|
| **Mon** | Env setup + Data pipeline scaffold                         |
| **Tue** | WordCount MR job coded & tested on sample data             |
| **Wed** | Lexicon loader + Sentiment MR job                          |
| **Thu** | Combine jobs into unified pipeline; optimize performance   |
| **Fri** | Full QA, edge‑case tests, finalize docs & handoff          |

---

## 4. Detailed Task Breakdown

### Day 1 (Mon)
- **E1:**  
  - Install/configure Hadoop or MRJob  
  - Provision Python 3.9, virtualenv, dependencies  
- **E2:**  
  - Define input formats (JSON, CSV, raw text); implement parser  
  - Build cleaning script (tokenization, lowercasing, punctuation removal)  
- **E3–E5 Sync:**  
  - Create Git repo skeleton:  
    ```
    /src
    /tests
    /data
    /docs
    ```  
  - Agree on code style, logging format, CLI interface spec  

### Day 2 (Tue)
- **E3:**  
  - `mapper_wordcount.py` (emit `<word, 1>`)  
  - `reducer_wordcount.py` (sum counts)  
  - Validate on small sample  
- **E2:**  
  - Hook cleaned data into MR job; launch script for Hadoop streaming or MRJob  
- **E5:**  
  - Unit tests for mapper and reducer  
  - Document CLI flags (`--input`, `--output`, `--job wordcount`)  

### Day 3 (Wed)
- **E4:**  
  - Load sentiment lexicon into memory (word → score/label)  
  - `mapper_sentiment.py` (emit `<doc_id, sentiment_score>`)  
  - `reducer_sentiment.py` (aggregate per‑doc or global breakdown)  
- **E2:**  
  - Tag each document with unique ID; feed into sentiment job  
- **E5:**  
  - Unit tests for lexicon loader and mapper logic  
  - Define thresholds for positive/negative/neutral  

### Day 4 (Thu)
- **E3 & E4:**  
  - `run_pipeline.py` to chain jobs:  
    ```bash
    #!/usr/bin/env python3
    # 1. WordCount job → counts.txt
    # 2. Sentiment job → sentiment_summary.txt
    ```  
  - Add parallel execution or job‑chaining support  
- **E1:**  
  - Tune job parameters (partitions, memory)  
- **E5:**  
  - Integration tests on mid‑sized corpus (e.g. 100 K tweets)  
  - Verify correctness and runtime  

### Day 5 (Fri)
- **E5 (lead):**  
  - Final QA: edge cases (empty docs, all neutral words, large files)  
  - Polish `README.md`: usage examples, dependencies, sample outputs  
  - Package code (Dockerfile or build script)  
- **All:**  
  - Final code review, merge branches, tag release v1.0  
  - Handoff deliverables to stakeholders  

---

## 5. Deliverables

1. **Source Code** (`/src/`):  
   - `mapper_wordcount.py`  
   - `reducer_wordcount.py`  
   - `mapper_sentiment.py`  
   - `reducer_sentiment.py`  
   - `run_pipeline.py`  
2. **Tests** (`/tests/`):  
   - Unit tests for mappers, reducers, lexicon loader  
   - Integration test scripts  
3. **Documentation** (`/docs/README.md`):  
   - Setup instructions  
   - Job invocation syntax & examples  
   - Performance tuning notes  
4. **Sample Data & Outputs** demonstrating word counts and sentiment analysis on a toy corpus  

