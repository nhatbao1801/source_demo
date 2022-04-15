# [eventcenter.api.hspace.biz](https://gitlab.com/hspace-biz/backend-team/eventcenter.api.hspace.biz.git)

Chào mừng bạn đến với eventcenter.api.hspace.biz 

## Hướng dẫn config ci => aws

1. Đổi file ```.env-sample``` thành file ```.env``` và sửa những config phù hợp với dự án của mình.
1. Tại Gitlab thì cần thêm những parameter tương ứng vd: SQL_DATABASE, SQL_HOST, PUBLIC_HOST_AWS, ... đại loại như thế
1. Tại aws/ec2, cần config nginx để chạy theo domain mình quy định. 
   *Lưu ý*: Tại nginx config file ```*.conf``` cần lưu ý ports mà bạn public ra khỏi container
   vd: của project hiện tại là map port ```80``` => ra ngoài ```1337```