# User Study (RQ2)

This folder contains:
- Study materials (`stimuli/` for explanation texts, `datasets/` for LLM-vs-human comparison JSONs).
- A minimal web app to collect human judgments for RQ2.
- `ground_truth.json` (snapshot of `python_defects` used to show the "Description of the code problem (after successful fixing)" to participants).
- `archive_revised_materials/` for superseded study inputs kept only for traceability.

## Local run (no cloud storage)

If `GCS_BUCKET` is not set, responses are stored locally under `USER_STUDY_LOCAL_DIR` (default: `/tmp/user_study_data`).

1) Install deps:

```bash
./venv/bin/python3 -m pip install -r user_study/requirements.txt
```

2) Run:

```bash
./venv/bin/python3 -m uvicorn user_study.app.main:app --host 0.0.0.0 --port 8080
```

3) Generate a local test link:

```bash
./venv/bin/python3 user_study/scripts/generate_tokens.py --n 1 --base-url http://localhost:8080
```

## Cloud Run deployment (GCS persistence)

Project: `<YOUR_GCP_PROJECT_ID>`
Region: `europe-west1`

### Current deployed resources (2026-02-11)

- Cloud Run service: `user-study` (region `europe-west1`)
- Service URL: `https://<YOUR_CLOUD_RUN_URL>`
- Container image: `europe-west1-docker.pkg.dev/<YOUR_GCP_PROJECT_ID>/containers/user-study:20260211T084438Z`
- GCS bucket (responses): `gs://<YOUR_GCS_BUCKET>` (writes under `user_study/state/` and `user_study/audit/`)
- Service account (runtime): `sa-user-study-run@<YOUR_GCP_PROJECT_ID>.iam.gserviceaccount.com`
- Artifact Registry repo: `containers` (location `europe-west1`)

### 1) Enable APIs

```bash
gcloud --project $PROJECT services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  storage.googleapis.com \
  iam.googleapis.com
```

### 2) Create bucket + service account

```bash
export PROJECT=<YOUR_GCP_PROJECT_ID>
export REGION=europe-west1
export BUCKET=<YOUR_GCS_BUCKET>

gcloud storage buckets create gs://$BUCKET --location=$REGION --uniform-bucket-level-access

gcloud --project $PROJECT iam service-accounts create sa-user-study-run --display-name="User study Cloud Run SA"
gcloud storage buckets add-iam-policy-binding gs://$BUCKET \
  --member=serviceAccount:sa-user-study-run@$PROJECT.iam.gserviceaccount.com \
  --role=roles/storage.objectAdmin
```

### 3) Create Artifact Registry repo

```bash
gcloud --project $PROJECT artifacts repositories create containers \
  --repository-format=docker \
  --location=$REGION \
  --description="Container images"
```

### 4) Build + deploy (redeploy)

```bash
export TAG=$(date -u +%Y%m%dT%H%M%SZ)
export IMAGE=$REGION-docker.pkg.dev/$PROJECT/containers/user-study:$TAG

gcloud --project $PROJECT builds submit user_study \
  --config user_study/cloudbuild.yaml \
  --substitutions _IMAGE=$IMAGE

gcloud --project $PROJECT run deploy user-study \
  --image $IMAGE \
  --region $REGION \
  --allow-unauthenticated \
  --service-account sa-user-study-run@$PROJECT.iam.gserviceaccount.com \
  --set-env-vars GCS_BUCKET=$BUCKET,APP_ENV=prod,GIT_SHA=$TAG
```

### 5) Generate participant links

```bash
export BASE_URL=$(gcloud --project $PROJECT run services describe user-study --region $REGION --format='value(status.url)')
./venv/bin/python3 user_study/scripts/generate_tokens.py --n 8 --base-url "$BASE_URL"
```

Notes:
- On the first page, the participant must enter a **Participant ID (or name)**; this value is stored in the saved JSON to avoid mixing results.

### 6) Export results

```bash
./venv/bin/python3 user_study/scripts/export_gcs.py --bucket $BUCKET
```

## Build Human vs LLM comparison dataset (LLM judge; default: GPT-5-mini)

This joins the exported participant labels (`user_study/results/*.json`) with **LLM-as-a-judge** labels for the
same explanation stimuli (`user_study/stimuli/defect*_py_BASELINE_run*.txt`) and writes a single comparison JSON dataset.

Important: A/B/C were randomized per participant. The mapping from **letter → run_id (1..3)** is stored in each
participant JSON under `assignment.explanation_map`, and the script uses that mapping when joining labels.

### Script behavior (concise)

- **Defaults:** `--backend openai --model gpt-5-mini --runs 3`
- **Inputs:** `ground_truth.json`, `results/*.json` (participant state exports), and `stimuli/defect*_py_BASELINE_run{1..runs}.txt`
- **Rows:** one per (participant × defect × A/B/C) → `n_rows = n_participants × n_defects × 3`
- **LLM calls:** the judge is called **once per row** (`judge.strategy="per_row"`) → `n_llm_calls = n_rows`
  - With 12 participants, 8 defects, 3 runs: `12 × 8 × 3 = 288` calls (intentional to sample judge nondeterminism)
- **Output:** JSON dataset (currently `schema_version: 2`) containing `rows`, `llm_explanations` (stimulus metadata), and summaries

### Usage

Requires `OPENAI_API_KEY` (for `--backend openai`) or `OPENROUTER_API_KEY` (for `--backend openrouter`) to be set.

Build dataset (writes output JSON; makes LLM calls):

```bash
./venv/bin/python3 user_study/scripts/build_human_vs_llm_dataset.py \
  --out user_study/datasets/human_vs_llm_gpt5mini.json
```

Dry-run (no LLM calls, no output; prints planned `n_rows` / `n_llm_calls`):

```bash
./venv/bin/python3 user_study/scripts/build_human_vs_llm_dataset.py --dry-run
```

Select a different judge backend/model (example):

```bash
./venv/bin/python3 user_study/scripts/build_human_vs_llm_dataset.py \
  --backend openrouter \
  --model deepseek/deepseek-v3.2
```

Verify the produced dataset (no LLM calls):

```bash
./venv/bin/python3 user_study/scripts/verify_human_vs_llm_dataset.py \
  --dataset user_study/datasets/human_vs_llm_gpt5mini.json
```

## Inspect what's saved in the bucket

```bash
export BUCKET=<YOUR_GCS_BUCKET>

# List everything saved for the study
gcloud storage ls -r gs://$BUCKET/user_study/

# List latest participant states (one JSON per token hash)
gcloud storage ls gs://$BUCKET/user_study/state/

# List append-only audit events
gcloud storage ls -r gs://$BUCKET/user_study/audit/

# Print a specific JSON (no download)
gcloud storage cat gs://$BUCKET/user_study/state/<token_sha256>.json | head
```

## Example saved JSON structure

The app stores one **merged state** JSON per participant token under `user_study/state/<token_sha256>.json`.

Example (abridged):

```json
{
  "schema_version": 2,
  "participant": {
    "created_at": "2026-02-10T21:36:55Z",
    "token_hash": "<sha256(token)>",
    "consent": true,
    "consented_at": "2026-02-10T21:37:02Z",
    "warmup_label_completed": true,
    "warmup_completed": true,
    "participant_id": "P07",
    "last_updated_at": "2026-02-10T21:42:18Z"
  },
  "assignment": {
    "defect_order": ["defect1_py", "defect4_py", "defect2_py"],
    "explanation_map": {
      "defect1_py": { "A": 2, "B": 1, "C": 3 },
      "defect4_py": { "A": 1, "B": 3, "C": 2 },
      "defect2_py": { "A": 3, "B": 2, "C": 1 }
    },
    "explanation_order": {
      "defect1_py": ["B", "A", "C"],
      "defect4_py": ["C", "A", "B"],
      "defect2_py": ["A", "C", "B"]
    }
  },
  "responses": {
    "initial_labels": {
      "defect1_py": {
        "A": { "C2": 1, "C3": 0, "C4": 1, "C6": 1 },
        "B": { "C2": 0, "C3": 0, "C4": 1, "C6": 0 },
        "C": { "C2": 1, "C3": 1, "C4": 1, "C6": 1 }
      }
    },
    "likert": {
      "defect1_py": { "C2": 4, "C3": 3, "C4": 5, "C6": 4 }
    }
  },
  "app": {
    "app_env": "prod",
    "git_sha": "20260210T213653Z"
  }
}
```

## Delete deployment (teardown)

⚠️ This deletes the Cloud Run service and (optionally) all stored participant data.

```bash
export PROJECT=<YOUR_GCP_PROJECT_ID>
export REGION=europe-west1
export BUCKET=<YOUR_GCS_BUCKET>

# 1) Delete the Cloud Run service
gcloud --project $PROJECT run services delete user-study --region $REGION

# 2) (Optional) Delete the Artifact Registry repo + all images
gcloud --project $PROJECT artifacts repositories delete containers --location $REGION --delete-contents

# 3) (Optional) Delete participant data + bucket
gcloud storage rm -r gs://$BUCKET/user_study/
gcloud storage buckets delete gs://$BUCKET

# 4) (Optional) Delete the service account
gcloud --project $PROJECT iam service-accounts delete sa-user-study-run@$PROJECT.iam.gserviceaccount.com
```
