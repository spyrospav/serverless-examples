# serverless-examples

## Import Time Measurement

Use the script `create_timed_file.py` to create timed version of each test cases. The result is printed in the form `<import FLOATING seconds>`, using the following regex to extract from the output:

```
<import\s([\d.]+)\sseconds>
```

It is provided in `extract_time.py`.