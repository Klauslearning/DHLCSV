
import streamlit as st
import pandas as pd
import os

# Set Streamlit page config
st.set_page_config(page_title="DHL CSV 生成器", layout="centered")

# Title
st.title("📦 DHL CSV 自动生成工具")
st.markdown("上传商品描述 Excel，系统将根据本地数据库生成 DHL 所需格式的 CSV 文件。")

# Load local reference databases from data/
@st.cache_data
def load_reference_data():
    sku_df = pd.read_csv("data/sku_reference_data.csv")
    fallback_df = pd.read_csv("data/fashion_commodity_codes.csv")
    return sku_df, fallback_df

sku_df, fallback_df = load_reference_data()

# Upload user file
desc_file = st.file_uploader("上传商品描述文件 (Description.xlsx)", type=["xlsx"])

if desc_file:
    try:
        df_desc = pd.read_excel(desc_file, sheet_name="Sheet1")
        st.success("✅ 文件上传成功！正在处理...")

        def match_sku(description):
            for _, row in sku_df.iterrows():
                if pd.notna(row['SKU']) and str(row['SKU']) in description:
                    return row['Commodity Code'], row['Weight (kg)'], row['Origin']
            return None, None, None

        def match_fallback(description):
            for _, row in fallback_df.iterrows():
                if str(row['Keyword']).lower() in description.lower():
                    return row['HS Code'], row['Default Weight'], row['Default Origin']
            return '', '', ''

        output_rows = []
        for desc in df_desc.iloc[:, 0]:
            hs_code, weight, origin = match_sku(desc)
            if not hs_code:
                hs_code, weight, origin = match_fallback(desc)

            row = {
                "Unique Item Number": 1,
                "Item": "INV_ITEM",
                "Item Description": desc,
                "Commodity Code": hs_code or '',
                "Quantity": 1,
                "Units": "PCS",
                "Value": 100,
                "Currency": "GBP",
                "Weight": weight or '',
                "Weight 2": "",
                "Country of Origin": origin or '',
                "Reference Type": "",
                "Reference Details": "",
                "Tax Paid": ""
            }
            output_rows.append(row)

        df_final = pd.DataFrame(output_rows)
        st.dataframe(df_final)

        csv_data = df_final.to_csv(index=False, header=False).encode('utf-8')
        st.download_button(
            label="📥 下载 DHL CSV 文件（无表头）",
            data=csv_data,
            file_name="DHL_ready_output.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"❌ 处理失败: {e}")
else:
    st.info("请上传包含商品描述的 Excel 文件（第一列为描述）。")
