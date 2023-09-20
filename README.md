# serverless-approve-workflow-demo


## 架构
![使用stepfunction的批准工作流程](/assets/approve_workflow.drawio.png)

## 部署：
1. 使用lambda的文件创建对应的lambda函数
2. 使用异步调用模板创建stepfunction
3. 修改对应参数
4. 使用lambda URL调用测试

## 演示
1. 使用客户端提交请求，请使用http post 方法提交
```
{
    "title": "休假申请",
    "request": "最近身体不舒服，请求休假3天，请老板批准"
}
```
![提交申请](/assets/demo1.png)

2

