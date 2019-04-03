# UcanToo
## Dual Encoder LSTM Model Generation
### Designed to run in Google Cloud
Command:
gcloud ml-engine jobs submit training JOB20 --module-name=trainer.model_generator --package-path=./trainer --job-dir=gs://ucantoo --region=us-central1 --runtime-version 1.13
