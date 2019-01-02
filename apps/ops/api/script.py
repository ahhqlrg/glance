# ~*~ coding: utf-8 ~*~

from rest_framework import viewsets, generics
from rest_framework_bulk import BulkModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from common.permissions import IsValidUser
from ..models import  Script
from ..serializers import ScriptCreateUpdateSerializer, ScriptListSerializer




class ScriptViewSet(BulkModelViewSet):
    """
      script授权列表的增删改查api
    """
    filter_fields = ('task_name','id')
    search_fields = filter_fields
    queryset = Script.objects.all()
    serializer_class = ScriptListSerializer
    permission_classes = (IsValidUser,)
    pagination_class = LimitOffsetPagination




    # def get_queryset(self):
    #     queryset = current_org.get_org_users()
    #     return queryset

    # def get_permissions(self):
    #     if self.action == "retrieve":
    #         self.permission_classes = (IsOrgAdminOrAppUser,)
    #     return super().get_permissions()
    #
    def allow_bulk_destroy(self, qs, filtered):
        return qs.count() == filtered.count()



    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        return Script.objects.filter(
           users=str(self.request.user.id)
        )


    # def get_serializer_class(self):
    #     if self.action in ("list", 'retrieve'):
    #         return ScriptListSerializer
    #     return ScriptListSerializer
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        asset_id = self.request.query_params.get('asset')
        node_id = self.request.query_params.get('node')
        inherit_nodes = set()
        if not asset_id and not node_id:
            return queryset

        permissions = set()
        if asset_id:
            asset = get_object_or_404(Asset, pk=asset_id)
            permissions = set(queryset.filter(assets=asset))
            for node in asset.nodes.all():
                inherit_nodes.update(set(node.get_ancestor(with_self=True)))
        elif node_id:
            node = get_object_or_404(Node, pk=node_id)
            permissions = set(queryset.filter(nodes=node))
            inherit_nodes = node.get_ancestor()

        for n in inherit_nodes:
            _permissions = queryset.filter(nodes=n)
            set_or_append_attr_bulk(_permissions, "inherit", n.value)
            permissions.update(_permissions)
        return permissions
    """