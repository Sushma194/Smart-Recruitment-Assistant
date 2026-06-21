import pandas as pd
import numpy as np

np.random.seed(42)

rows = 500

data = {
    "Candidate_ID": range(1, rows + 1),
    "CGPA": np.round(np.random.uniform(5.5, 10.0, rows), 2),
    "Aptitude": np.random.randint(40, 100, rows),
    "Technical": np.random.randint(40, 100, rows),
    "Communication": np.random.randint(40, 100, rows),
    "Certifications": np.random.randint(0, 6, rows),
    "Internships": np.random.randint(0, 4, rows),
    "Projects": np.random.randint(1, 8, rows),
    "Experience": np.random.randint(0, 6, rows),
    "Interview": np.random.randint(40, 100, rows)
}

df = pd.DataFrame(data)

score = (
    df["CGPA"] * 5 +
    df["Technical"] * 0.30 +
    df["Communication"] * 0.20 +
    df["Interview"] * 0.30 +
    df["Projects"] * 2 +
    df["Internships"] * 3
)

df["Selected"] = (score > score.median()).astype(int)

df.to_csv("data/recruitment_data.csv", index=False)

print("Dataset Created Successfully")