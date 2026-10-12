# Hướng dẫn mở bài

Thư mục chính gồm báo cáo PDF, notebook Python, Power BI, dữ liệu gốc và dữ liệu sạch. Bản Word nằm trong Tai_lieu_kem_theo. Giải nén toàn bộ bài vào ổ D hoặc E trên máy Windows, giữ nguyên cấu trúc thư mục.

Tai_lieu_kem_theo chứa ảnh, code Streamlit, danh sách thư viện và file mở dashboard.

## Báo cáo

Mở BaoCao_NguyenHaiDang_B23DCKD010.pdf ở thư mục chính. Bản Word là Tai_lieu_kem_theo/BaoCao_NguyenHaiDang.docx. Các hình đã được nhúng trong Word; ảnh riêng nằm trong Tai_lieu_kem_theo/hinh_ve.

## Notebook

Mở Python_NguyenHaiDang.ipynb bằng VS Code hoặc Jupyter. Dùng Python 3.12 và cài thư viện trong Tai_lieu_kem_theo/requirements_notebook.txt. Chạy các ô từ trên xuống. Notebook và hai CSV phải nằm cùng thư mục chính.

## Streamlit

Mở Tai_lieu_kem_theo/Mo_dashboard.cmd. Máy cần Python 3.11 trở lên; bài đã được kiểm tra với Python 3.12. Lần đầu cần Internet để tự cài thư viện. Giữ cửa sổ chạy và trang dashboard mở. Code nằm trong Tai_lieu_kem_theo/dashboard_streamlit; thư viện nằm trong requirements.txt tại cùng thư mục code.

Dashboard đọc marketing_clean_powerbi.csv ở thư mục chính và đọc lại mỗi 30 giây khi phiên đang mở. Khi dữ liệu gốc thay đổi, chạy lại notebook để xuất CSV sạch trước.

## Power BI

Mở PowerBI_NguyenHaiDang.pbix ở thư mục chính bằng Power BI Desktop. Khi chuyển máy hoặc thư mục, chọn lại nguồn marketing_clean_powerbi.csv trong thư mục chính trước khi Refresh.