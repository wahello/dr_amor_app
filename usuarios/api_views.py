from django.contrib.auth.models import User, Permission, Group
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from knox.models import AuthToken
from rest_framework import viewsets, generics, permissions, serializers
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from permisos.api_serializers import PermissionSerializer
from .api_serializers import UsuarioSerializer, LoginUserSerializer, UserSerializer
from puntos_venta.models import PuntoVenta
from puntos_venta.api_serializers import PuntoVentaSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer

    @list_route(methods=['get'])
    def mi_cuenta(self, request):
        qs = self.get_queryset().filter(
            id=request.user.id
        ).distinct()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def adicionar_permiso(self, request, pk=None):
        usuario = self.get_object()
        id_permiso = int(request.POST.get('id_permiso'))
        permiso = Permission.objects.get(id=id_permiso)

        tiene_permiso = usuario.user_permissions.filter(id=id_permiso).exists()
        if not tiene_permiso:
            usuario.user_permissions.add(permiso)
        else:
            usuario.user_permissions.remove(permiso)

        serializer = self.get_serializer(usuario)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def adicionar_grupo(self, request, pk=None):
        usuario = self.get_object()
        id_grupo = int(request.POST.get('id_grupo'))
        permiso = Group.objects.get(id=id_grupo)

        tiene_grupo = usuario.groups.filter(id=id_grupo).exists()
        if not tiene_grupo:
            usuario.groups.add(permiso)
        else:
            usuario.groups.remove(permiso)

        serializer = self.get_serializer(usuario)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def cambiar_pin(self, request, pk=None):
        usuario = self.get_object()
        pin = request.POST.get('pin')
        password = request.POST.get('password')
        if usuario.check_password(password):
            if hasattr(usuario, 'tercero'):
                usuario.tercero.set_new_pin(pin)
            return Response({'result': 'El pin se ha cambiado correctamente'})
        else:
            raise serializers.ValidationError({'error': 'La contraseña suministrada no coincide con el usuario'})

    @detail_route(methods=['post'])
    def cambiar_contrasena(self, request, pk=None):
        usuario = self.get_object()
        password_old = request.POST.get('password_old')
        password = request.POST.get('password')
        password_2 = request.POST.get('password_2')
        if usuario.check_password(password_old):
            if password == password_2:
                usuario.set_password(password)
                usuario.save()
                return Response({'result': 'La contraseña se ha cambiado correctamente'})
            else:
                raise serializers.ValidationError({'error': 'La contraseña nueva con su confirmación no coincide'})
        else:
            raise serializers.ValidationError({'error': 'La contraseña suministrada no coincide con el usuario'})

    @list_route(methods=['get'])
    def validar_nuevo_usuario(self, request) -> Response:
        qs = self.get_queryset()
        validacion_reponse = {}
        username = self.request.GET.get('username', None)
        if username and qs.filter(username=username).exists():
            validacion_reponse.update({'username': 'Ya exite'})
        return Response(validacion_reponse)

    @list_route(methods=['get'], permission_classes=[permissions.AllowAny])
    def validar_username_login(self, request) -> Response:
        qs = self.get_queryset()
        validacion_reponse = {}
        username = self.request.GET.get('username', None)
        if username and not qs.filter(username=username).exists():
            validacion_reponse.update({'username': 'Este usuario no existe'})
        return Response(validacion_reponse)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        punto_venta_id = request.data.pop('punto_venta')
        try:
            punto_venta = PuntoVenta.objects.get(pk=punto_venta_id)
        except ObjectDoesNotExist:
            punto_venta = None
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        if punto_venta:
            if punto_venta.abierto and not punto_venta.usuario_actual == user:
                raise serializers.ValidationError(
                    {'error': ['%s tiene abierto este Punto de Venta!' % punto_venta.usuario_actual.username]}
                )
            else:
                punto_venta.abierto = True
                punto_venta.usuario_actual = user
                punto_venta.save()

        tokens = AuthToken.objects.filter(user=user)
        tokens.delete()

        if user.is_superuser:
            permissions_list = Permission.objects.all()
        else:
            permissions_list = Permission.objects.filter(
                Q(user=user) |
                Q(group__user=user)
            ).distinct()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user),
            "punto_venta": PuntoVentaSerializer(punto_venta, context=self.get_serializer_context()).data,
            "mi_cuenta": UsuarioSerializer(user, context=self.get_serializer_context()).data,
            "mis_permisos": PermissionSerializer(permissions_list, context=self.get_serializer_context(),
                                                 many=True).data,
        })


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
