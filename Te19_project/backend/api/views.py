from django.shortcuts import render
import json
import boto3
from django.http import JsonResponse


def index(request):
    return render(request, 'index.html')


AWS_REGION = "ap-southeast-2"   
BUCKET     = "5120onboarding"  

CUR_VEHICLE_KEY = "curated/vehicle_growth.json"
CUR_POP_KEY     = "curated/cbd_population.json"

s3 = boto3.client("s3", region_name=AWS_REGION)

def _s3_json(key: str):
    obj = s3.get_object(Bucket=BUCKET, Key=key)
    return json.loads(obj["Body"].read())

def vehicle_growth(request):
    return JsonResponse(_s3_json(CUR_VEHICLE_KEY), safe=False)

def cbd_population(request):
    return JsonResponse(_s3_json(CUR_POP_KEY), safe=False)
