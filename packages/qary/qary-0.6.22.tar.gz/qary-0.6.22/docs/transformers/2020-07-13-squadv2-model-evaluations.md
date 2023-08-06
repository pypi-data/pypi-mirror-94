Summary of evaluation metrics obtained by submitting predictions by different models on the SQuAD hold-out set on SQuAD website:

| MODEL |finetuned|  exact | f1 | total | HasAns_exact | HasAns_f1 | HasAns_total | NoAns_exact | NoAns_f1 | NoAns_total 
|-------|---------|--------|----|-------|--------------|-----------|-------------|-------------|----------|------------  
human performance|NA|86.831|89.452|NA|NA|NA|NA|NA|NA|NA
albert-base-v2|NA|18.38|19.13|11873|0.05|1.55|5928|36.65|36.65|5945
albert-xxlarge-v2|NA|0.008|0.64|11873|0|1.26|5928|0.017|0.017|5945
bert_base_uncased|squad|25.16|26.22|11873|0.84|2.96|5928|49.4|49.4|5945
distilbert-ba|Travis|56.77|59.17|11873|46.27|51.07|5928|67.24|67.24|5945
bert-ba|Travis|62.58|65.52|11873|48.98|54.87|5928|76.14|76.14|5945
albert-lg|Travis|63.56|65.12|11873|34.90|38.03|5928|92.14|92.1|5945
bert-tiny|mrm8488, squad2|35.11|35.11|11873|0.15|0.34|5928|69.97|69.97|5945
albert-base-v2|twmkn9, squad2|77.92|81.38|11873|72.84|79.78|5928|82.98|82.98|5945
albert-xlarge-v2|ktrapeznikov, squad2|84.46|87.47|11873|80.01|86.04|5928|88.90|88.90|5945
