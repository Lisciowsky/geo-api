from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from api.geo import request_geo_info
from api.serializers import GEOSerializer
from api.models import GEO


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_overview(request):
    api_urls = {
        "list": "/geo-list/",
        "detail": "/geo-detail/<str:pk>",
        "create": "/geo-create/",
        "update": "task-update/<str:pk>",
        "delete": "/task-delete/<str:pk>",
    }
    return Response(api_urls)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def geo_list(request):
    geo = request.user.geos.all()
    serializer = GEOSerializer(geo, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def geo_detail(request, pk):
    geo = get_object_or_404(GEO, id=pk, user=request.user)
    serializer = GEOSerializer(geo, many=False)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def geo_create(request):
    serializer = GEOSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    address = GEO.normilize_address(serializer.validated_data["address"])

    try:
        obj = GEO.objects.get(address=address, user=request.user)
        serializer = GEOSerializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except GEO.DoesNotExist:
        try:
            api_info = request_geo_info(address).json()
            if not api_info["success"]:
                return Response(api_info, status=status.HTTP_400_BAD_REQUEST)

            longitude = api_info["longitude"]
            latitude = api_info["latitude"]
            serializer.save(
                longitude=longitude,
                latitude=latitude,
                user=request.user,
                address=address,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except:
            return Response(
                {"detail": "service is not available"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def geo_update(request, pk):
    geo = get_object_or_404(GEO, id=pk, user=request.user)
    serializer = GEOSerializer(geo, data=request.data)
    serializer.is_valid(raise_exception=True)
    address = GEO.normilize_address(serializer.validated_data["address"])

    try:
        ip_info = request_geo_info(address).json()
        if not ip_info["success"]:
            return Response(ip_info, status=status.HTTP_404_NOT_FOUND)

        longitude = ip_info["longitude"]
        latitude = ip_info["latitude"]
        serializer.save(
            longitude=longitude, latitude=latitude, user=request.user, address=address
        )
        return Response(serializer.data)

    except:
        return Response(
            {"detail": "service is not available"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def geo_delete(request, pk):
    geo = get_object_or_404(GEO, id=pk, user=request.user)
    geo.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
