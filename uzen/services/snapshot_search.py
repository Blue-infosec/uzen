from tortoise.query_utils import Q
import datetime


from uzen.models import Snapshot


def convert_to_datetime(s: str) -> datetime.datetime:
    return datetime.datetime.strptime(s, "%Y-%m-%d")


class SnapshotSearcher:

    @staticmethod
    async def search_all(query, id_only=False):
        if id_only:
            return await Snapshot.filter(query).order_by("-id").values_list("id", flat=True)

        return await Snapshot.filter(query).order_by("-id")

    @staticmethod
    async def search_with_size(query, size=100, id_only=False):
        if id_only:
            return await Snapshot.filter(query).order_by("-id").limit(size).values_list("id", flat=True)

        return await Snapshot.filter(query).order_by("-id").limit(size)

    @staticmethod
    async def search_with_size_and_offset(query, offset=0, size=100, id_only=False):
        if id_only:
            return await Snapshot.filter(query).order_by("-id").offset(offset).limit(size).values_list("id", flat=True)

        return await Snapshot.filter(query).order_by("-id").offset(offset).limit(size)

    @staticmethod
    async def search(filters, size=None, offset=None, id_only=False):
        queries = []

        hostname = filters.get("hostname")
        if hostname is not None:
            queries.append(Q(hostname__contains=hostname))

        ip_address = filters.get("ip_address")
        if ip_address is not None:
            queries.append(Q(ip_address__contains=ip_address))

        server = filters.get("server")
        if server is not None:
            queries.append(Q(server__contains=server))

        content_type = filters.get("content_type")
        if content_type is not None:
            queries.append(Q(content_type__contains=content_type))

        from_at = filters.get("from_at")
        if from_at is not None:
            from_at = convert_to_datetime(from_at)
            queries.append(Q(created_at__gte=from_at))

        to_at = filters.get("to_at")
        if to_at is not None:
            to_at = convert_to_datetime(to_at)
            queries.append(Q(created_at__lte=to_at))

        query = Q(*queries)

        if size is not None and offset is None:
            return await SnapshotSearcher.search_with_size(query, size=size, id_only=id_only)
        elif offset is not None:
            if size is None:
                size = 100
            return await SnapshotSearcher.search_with_size_and_offset(query, size=size, offset=offset, id_only=id_only)

        return await SnapshotSearcher.search_all(query, id_only=id_only)