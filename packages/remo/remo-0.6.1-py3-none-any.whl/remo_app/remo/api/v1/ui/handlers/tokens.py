import json

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from remo_app.remo.services.license import read_license
from remo_app.remo.services.license import store_token, invalidate_existing_token, refresh_token


class Tokens(viewsets.GenericViewSet):
    def list(self, request, *args, **kwargs):
        return Response({})

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'not allowed action'}, status=status.HTTP_403_FORBIDDEN)

        try:
            data = json.loads(request.body)
        except Exception:
            return Response({'error': 'failed to parse payload'}, status=status.HTTP_400_BAD_REQUEST)

        token = data.get('token', '')
        if not token:
            return Response({'error': 'token was not set'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'valid': store_token(token)}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'not allowed action'}, status=status.HTTP_403_FORBIDDEN)

        try:
            invalidate_existing_token()
        except Exception as err:
            return Response({'error': f'failed to delete token, {err}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['get'], detail=True, url_path='refresh')
    def refresh(self, request, pk=None):
        if not request.user.is_superuser:
            return Response({'error': 'not allowed action'}, status=status.HTTP_403_FORBIDDEN)

        refresh_token()
        return Response(read_license().to_dict(), status=status.HTTP_200_OK)
