# Bài tập lớn Trực quan hóa dữ liệu

**Đề tài:** Trực quan hóa và phân tích dữ liệu khách hàng trong hoạt động marketing.

**Sinh viên:** Nguyễn Hải Đăng — B23DCKD010.

Bài làm sử dụng bộ dữ liệu Customer Personality Analysis để phân tích hồ sơ khách hàng, chi tiêu sản phẩm, kênh mua, phản hồi marketing và mối liên hệ giữa thu nhập với chi tiêu.

## Các file chính

| File / thư mục | Nội dung |
| --- | --- |
| [BaoCao_NguyenHaiDang_B23DCKD010.pdf](BaoCao_NguyenHaiDang_B23DCKD010.pdf) | Báo cáo hoàn chỉnh |
| [Python_NguyenHaiDang.ipynb](Python_NguyenHaiDang.ipynb) | Xử lý dữ liệu, bảng thống kê và sáu hình Python |
| [PowerBI_NguyenHaiDang.pbix](PowerBI_NguyenHaiDang.pbix) | Hai trang dashboard Power BI |
| [marketing_campaign.csv](marketing_campaign.csv) | Dữ liệu gốc |
| [marketing_clean_powerbi.csv](marketing_clean_powerbi.csv) | Dữ liệu sạch dùng chung cho dashboard |
| [Tai_lieu_kem_theo](Tai_lieu_kem_theo) | Bản Word, code Streamlit, hình và thư viện |

## Quy trình

1. Xác định bài toán và câu hỏi phân tích.
2. Nạp và kiểm tra dữ liệu gốc.
3. Điền Income thiếu bằng trung vị theo Education; sau đó lọc tuổi và thu nhập bất thường.
4. Tính tuổi, số con, tổng chi tiêu và chia ba nhóm chi tiêu bằng qcut.
5. Vẽ sáu hình phân tích và xuất CSV sạch gồm 23 cột.
6. Trình bày kết quả bằng dashboard Streamlit–Plotly tự đọc lại CSV mỗi 30 giây; Power BI bổ sung hai trang tổng quan và hồ sơ.

Sau xử lý còn **2.236 khách hàng**, tổng chi tiêu **1.354.986**, thu nhập trung bình **51.957,24** và **334 người phản hồi (14,94%)**. Tuổi được tính theo năm 2014 của bộ dữ liệu.

## Tải và mở bài

Trên GitHub, chọn **Code → Download ZIP**, giải nén toàn bộ thư mục. Với bộ mở dashboard đi kèm, đặt thư mục trên ổ **D hoặc E** của máy Windows.

- **Báo cáo:** mở PDF ở thư mục chính; bản Word nằm trong Tai_lieu_kem_theo.
- **Notebook:** dùng Python 3.12, VS Code hoặc Jupyter; cài thư viện bằng lệnh dưới đây rồi mở notebook và chạy từ trên xuống. Hai CSV phải nằm cạnh notebook.

~~~powershell
python -m pip install -r Tai_lieu_kem_theo/requirements_notebook.txt
~~~

- **Streamlit:** cài Python 3.11 trở lên (bài đã chạy với Python 3.12), mở Tai_lieu_kem_theo/Mo_dashboard.cmd. Lần đầu cần Internet để cài thư viện. Giữ cửa sổ chạy và trang dashboard mở.
- **Power BI:** mở PBIX bằng Power BI Desktop. Khi chuyển máy, chọn lại nguồn marketing_clean_powerbi.csv trong thư mục chính trước khi Refresh.

Khi dữ liệu gốc thay đổi, cần chạy lại notebook để tạo CSV sạch mới trước khi xem dashboard.

## Nguồn dữ liệu

[Customer Personality Analysis — Kaggle](https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis).

Tài liệu tham khảo và nhận xét phân tích được trình bày trong báo cáo.
