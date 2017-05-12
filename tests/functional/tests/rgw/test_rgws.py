import pytest


class TestRGWs(object):

    @pytest.mark.no_docker
    def test_ceph_rgw_package_is_installed(self, node, Package):
        # ceph-radosgw is the package name on centos, radosgw is the name on ubuntu
        has_ceph_radosgw = Package("ceph-radosgw").is_installed
        has_radosgw = Package("radosgw").is_installed
        assert (has_ceph_radosgw or has_radosgw)

    def test_rgw_services_are_running(self, node, Service):
        service_name = "ceph-radosgw@rgw.ceph-{hostname}".format(
            hostname=node["vars"]["inventory_hostname"]
        )
        assert Service(service_name).is_running

    def test_rgw_services_are_enabled(self, node, Service):
        service_name = "ceph-radosgw@rgw.ceph-{hostname}".format(
            hostname=node["vars"]["inventory_hostname"]
        )
        assert Service(service_name).is_enabled

    @pytest.mark.no_docker
    def test_rgw_http_endpoint(self, node, Interface, Socket):
        # rgw frontends ip_addr is configured on eth0
        ip_addr = Interface("eth0").addresses[0]
        assert Socket("tcp://{ip_addr}:{port}".format(ip_addr=ip_addr, port=8080)).is_listening
