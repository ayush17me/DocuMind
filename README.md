# DocuMind
Use Python 3.11. Install with `pip install -r requirements.txt`. Set GOOGLE_API_KEY in your environment, then run `streamlit run app.py`. Upload selectable-text PDFs. D2-p3.1700 means document 2, page 3, chunk starting at character 1700. Indexes and the last conversation live in the browser's server-side session and are lost on disconnect or instance replacement.

## Cloud Run
From this folder in a billing-enabled Google Cloud project, configure gcloud's project, enable Cloud Run, Cloud Build, Artifact Registry and Secret Manager. Create a Secret Manager secret named gemini-api-key and grant the runtime service account access to it. With build and deployment permissions, run:
```sh
gcloud run deploy documind --source . --region asia-south1 --no-allow-unauthenticated --set-secrets GOOGLE_API_KEY=gemini-api-key:latest --memory 1Gi --timeout 3600
gcloud run services proxy documind --region asia-south1
```
Open the proxy URL with an identity holding Cloud Run Invoker. The service sends extracted text to Google's embedding service and retrieved passages to Gemini. Use approved documents.

## Evaluation
With the same key exported, run `python evaluate.py > results.jsonl`. Four synthetic questions run with and without verification. Compare hit_at_4 on the three answerable questions, reference_match, abstention on the missing fact, and total_ms. Inspect each answer against the fixture: mark every factual claim supported or unsupported and report supported claims divided by total factual claims. Score refusals separately so abstaining on everything cannot inflate faithfulness. A verifier PASS is a model judgment. Repeat on representative documents before reporting improvements.

Set INPUT_USD_PER_M and OUTPUT_USD_PER_M to your model's applicable per-million-token rates to estimate generation cost (excluding embeddings, hosting and special pricing). Missing rates yield null. Request logs contain stage timings, source IDs, usage and failure stage, without document or chat text. Evaluation explicitly prints its synthetic answers.
