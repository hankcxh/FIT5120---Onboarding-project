# scripts/curate_from_s3.py
from pathlib import Path
import io, json
import pandas as pd
import boto3

AWS_REGION = "ap-southeast-2"         
BUCKET     = "5120onboarding"      

# CSV（S3 raw/）
RAW_VEHICLE_KEY    = "raw/vehicle_data.csv"
RAW_POPULATION_KEY = "raw/population_data_cleaned.csv"

# output JSON（S3 curated/）
CUR_VEHICLE_KEY    = "curated/vehicle_growth.json"
CUR_POP_KEY        = "curated/cbd_population.json"

VEHICLE_GROUP = "TOTAL MOTOR VEHICLES"

s3 = boto3.client("s3", region_name=AWS_REGION)

def _read_csv_from_s3(key: str) -> pd.DataFrame:
    obj = s3.get_object(Bucket=BUCKET, Key=key)
    return pd.read_csv(io.BytesIO(obj["Body"].read()))

def _write_json_to_s3(key: str, payload: dict):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    s3.put_object(Bucket=BUCKET, Key=key, Body=body, ContentType="application/json")
    print(f" Wrote s3://{BUCKET}/{key}")

# Victoria car
def curate_vehicle_growth():
    df = _read_csv_from_s3(RAW_VEHICLE_KEY)

    df.rename(columns={c: c.strip() for c in df.columns}, inplace=True)

    # important row check
    need_cols = {"year", "vehicle_type_group", "Victoria"}
    missing = need_cols - set(df.columns)
    if missing:
        raise ValueError(f"vehicle_data.csv 缺少列: {missing}")

    
    sub = df[df["vehicle_type_group"] == VEHICLE_GROUP]

    sub = (sub[["year", "Victoria"]]
           .groupby("year", as_index=False)["Victoria"].sum()
           .sort_values("year"))
    sub.rename(columns={"Victoria": "registrations"}, inplace=True)

    series = sub.to_dict(orient="records")
    first, last = series[0]["registrations"], series[-1]["registrations"]
    total_growth = (last - first) / first if first else 0.0
    peak_year = max(series, key=lambda r: r["registrations"])["year"]
    trend = "up" if last > first else ("down" if last < first else "flat")

    payload = {
        "meta": {
            "region": "Victoria",
            "type_group": VEHICLE_GROUP,
            "total_growth": total_growth,
            "peak_year": peak_year,
            "trend_direction": trend
        },
        "series": series
    }
    _write_json_to_s3(CUR_VEHICLE_KEY, payload)

def curate_cbd_population():
    df = _read_csv_from_s3(RAW_POPULATION_KEY)

    #VIC
    if "ST_name" in df.columns:
        df = df[df["ST_name"] == "Victoria"]

    # only melbourne cbd
    if "SA2_name" not in df.columns:
        raise ValueError("population_data_cleaned.csv 缺少列 SA2_name")

    cbd = df[df["SA2_name"].str.contains("Melbourne CBD", na=False)].copy()
    if cbd.empty:
        raise ValueError("没有匹配到 SA2_name 包含 'Melbourne CBD' 的行，请检查原始数据。")

    #
    years = [str(y) for y in range(2016, 2022)]
    for y in years:
        if y not in cbd.columns:
            raise ValueError(f"人口CSV缺少年份列: {y}")

    series = [{"year": int(y), "population": float(cbd[y].sum())} for y in years]

    first, last = series[0]["population"], series[-1]["population"]
    growth_rate = (last - first) / first if first else 0.0

    pop_density_2021 = None
    if "Area" in cbd.columns:
        total_area = float(cbd["Area"].sum())
        if total_area > 0:
            pop_density_2021 = last / total_area

    payload = {
        "meta": {
            "region": "Melbourne CBD",
            "growth_rate": growth_rate,
            "population_density_2021": pop_density_2021,
            "note": "Aggregated from SA2_name ∈ {Melbourne CBD - East/North/West}."
        },
        "series": series
    }
    _write_json_to_s3(CUR_POP_KEY, payload)

if __name__ == "__main__":
    print("Curating vehicle growth ...")
    curate_vehicle_growth()
    print("Curating CBD population ...")
    curate_cbd_population()
    print("All curated JSON written to S3 curated/")
