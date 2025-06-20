# 手动开票服务使用说明

本项目实现了一个基于 **FastAPI** 和 **SQLite** 的简易开票服务，支持根据用户提供的商品或服务信息生成发票并导出 PDF 文件。

## 安装与运行
1. 进入项目目录，确保使用 Python 3.11 及以上版本。
2. 由于环境限制，项目已内置最简易的 PDF 生成逻辑，无需额外安装第三方库。
3. 启动服务：
   ```bash
   uvicorn app.main:app --reload
   ```

## API 说明
### `POST /invoices`
创建发票并返回结果。

请求示例：
```json
{
  "items": [
    {"name": "ItemA", "quantity": 2, "unit_price": 10.0},
    {"name": "ItemB", "quantity": 1, "unit_price": 20.0}
  ],
  "notes": "示例备注"
}
```

返回示例：
```json
{
  "id": 1,
  "subtotal": 40.0,
  "total_tax": 6.0,
  "total": 46.0,
  "pdf_path": "invoices/invoice_1.pdf",
  "items": [
    {"name": "ItemA", "quantity": 2, "unit_price": 10.0, "total": 20.0},
    {"name": "ItemB", "quantity": 1, "unit_price": 20.0, "total": 20.0}
  ]
}
```

### `GET /invoices/{id}`
下载生成的 PDF 文件。

## 测试
在项目根目录运行：
```bash
pytest
```

## 目录结构
- `app/`：核心代码
- `tests/`：单元测试
- `invoice_service_requirements.md`：需求文档

