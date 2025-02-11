import xml.etree.ElementTree as ET
from datetime import datetime
import codecs

def process_xml(input_file, template_file):
    try:
        # 讀取包含資料的 XML 檔案
        with codecs.open(input_file, 'r', encoding='big5') as f:
            content = f.read()
        
        # 解析 XML
        source_root = ET.fromstring(content)
        source_order = source_root.find('.//Order')
        
        if source_order is not None:
            deal_acc = source_order.get('DealAcc', '')
            deal_acc_ui = source_order.get('DealAccUI', '')
            ssid = source_order.get('SSID', '')
            
            print(f"讀取到的資料：")
            print(f"DealAcc: {deal_acc}")
            print(f"DealAccUI: {deal_acc_ui}")
            print(f"SSID: {ssid}")
            
            # 嘗試不同的編碼方式讀取模板文件
            encodings = ['big5', 'utf-8', 'cp950']
            template_content = None
            
            for encoding in encodings:
                try:
                    with open(template_file, 'r', encoding=encoding) as f:
                        template_content = f.read()
                        break
                except UnicodeDecodeError:
                    continue
            
            if template_content is None:
                # 如果上述編碼都失敗，嘗試二進制讀取
                with open(template_file, 'rb') as f:
                    template_content = f.read().decode('big5', errors='replace')
            
            template_root = ET.fromstring(template_content)
            
            # 更新所有 Order 標籤中的值
            for template_order in template_root.findall('.//Order'):
                template_order.set('DealAcc', deal_acc)
                template_order.set('DealAccUI', deal_acc_ui)
                template_order.set('SSID', ssid)
            
            # 生成新檔名
            current_time = datetime.now()
            new_filename = f"input_{ssid}_{current_time.strftime('%Y%m%d_%H%M')}.xml"
            
            # 將更新後的 XML 轉換為字串
            xml_str = ET.tostring(template_root, encoding='unicode')
            
            # 保存新文件，使用 errors='replace' 處理編碼問題
            with open(new_filename, 'w', encoding='big5', errors='replace') as f:
                f.write('<?xml version="1.0" encoding="big5"?>\n')
                f.write(xml_str)
            
            print(f"\n已生成新文件：{new_filename}")
            return new_filename
        else:
            print("錯誤：未找到 Order 標籤")
            return None
            
    except Exception as e:
        print(f"發生錯誤：{str(e)}")
        return None

# 測試代碼
if __name__ == "__main__":
    input_file = "output.xml"  # 包含資料的 XML 文件
    template_file = "1_27749_cppack.xml"  # 模板 XML 文件
    
    new_file = process_xml(input_file, template_file)
    if new_file:
        print("處理完成")