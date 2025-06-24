# 📦 DHL CSV Generator

自动化生成符合 DHL 上传格式的发货 CSV 文件，适用于**时尚商品代购（手袋、鞋、配饰、服装）**等跨境电商场景。

---

## 🚀 功能亮点

- ✅ 从商品描述中提取 SKU、品牌、关键词
- ✅ 自动匹配海关编码（Commodity Code）
- ✅ 自动估算重量（基于产品类型）
- ✅ 自动补全原产国（如有 SKU 映射表）
- ✅ 输出符合 DHL 要求的无表头 `.csv` 文件
- ✅ 可视化 GUI 支持（使用 Streamlit）

---

## 📂 输入文件说明

你需要准备以下文件，并放在同一个目录：

| 文件名 | 内容说明 |
|--------|----------|
| `Description.xlsx` | 客户下单信息，**第一列**为商品描述 |
| `sku_reference_data.csv` | SKU 对应的编码、重量、产地（可持续维护） |
| `fashion_commodity_codes.csv` | 关键词 fallback 映射表（如 bag → 4202.21.00） |

---

## 🧑‍💻 使用方式（命令行模式）

1. 安装依赖（推荐虚拟环境中操作）：

```bash
pip install pandas openpyxl
```

2. 运行脚本：

```bash
python dhl_csv_generator.py
```

3. 输出文件：

```
DHL_ready_output.csv
```

该文件为**无表头**, **14 列字段**, 可直接上传至 DHL。

---

## 🌐 GUI 模式（Streamlit）

如果你希望更友好地上传文件并一键生成，可使用 Streamlit：

1. 安装依赖：

```bash
pip install streamlit pandas openpyxl
```

2. 启动 GUI 应用：

```bash
streamlit run app.py
```

---

## 🧠 字段自动化逻辑说明

| 字段 | 自动处理逻辑 |
|------|---------------|
| `Commodity Code` | 优先匹配 SKU 映射，否则用关键词 fallback |
| `Weight` | 从 SKU 表获取，否则按关键词估算（如 bag=0.8kg） |
| `Origin` | 从 SKU 表匹配产地，否则留空 |
| `Value` | 默认填 100（可扩展从原始表提取） |
| 其他字段 | 固定值或留空，符合 DHL 要求格式 |

---

## 📈 后续扩展建议

- 多 SKU 每行识别（支持数量分拆）
- 支持品牌 + SKU → 自动查产地（数据库维护或 Web 抓取）
- 支持价格、Reference Type、Tax Paid 等补充字段
- 云端部署（Streamlit Cloud 或内网服务器）

---

## 🧾 示例输出格式（无表头）

```
1,INV_ITEM,LOUIS VUITTON SPEEDY 25 BAG,4202.21.00,1,PCS,1500,GBP,0.8,,FR,,,
```

---

## 📬 联系我

如需协助部署或功能定制，请联系项目作者。


