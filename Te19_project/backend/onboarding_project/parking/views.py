from django.shortcuts import render
from django.http import JsonResponse
from .models import ParkingZone
from django.db.models import Max
from django.utils.timezone import now
# Create your views here.


def parking_map(request):
    return render(request, "parking/map.html")


def zones_in_bbox(request):
    """
    GET /api/zones?bbox=minLon,minLat,maxLon,maxLat
    Returns zones with available/total + coords.
    """
    bbox = request.GET.get("bbox")
    if not bbox:
        return JsonResponse({"error": "bbox required"}, status=400)
    try:
        minx, miny, maxx, maxy = map(float, bbox.split(","))
    except Exception:
        return JsonResponse({"error": "invalid bbox"}, status=400)

    qs = ParkingZone.objects.filter(
        lon__gte=minx, lon__lte=maxx, lat__gte=miny, lat__lte=maxy
    )
    results = [{
        "zone_number": z.zone_number,
        "street": z.street_name,
        "coords": {"lat": z.lat, "lon": z.lon},
        "total_spots": z.total_spots,
        "available_spots": z.available_spots,
        "latest_update": z.latest_update.isoformat() if z.latest_update else None
    } for z in qs[:1000]]
    return JsonResponse({"results": results})
def status(request):
    latest = ParkingZone.objects.aggregate(mx=Max("latest_update"))["mx"]
    return JsonResponse({
        "server_time": now().isoformat(),
        "latest_update_in_db": latest.isoformat() if latest else None,
        "zones_with_data": ParkingZone.objects.filter(available_spots__isnull=False).count(),
    })
