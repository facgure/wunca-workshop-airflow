# WUNCA A-Z Workshop
Repository สำหรับการ workshop การจัดการและการทำ Data Pipeline โดยใช้ Apache Airflow

สำหรับการเริ่มต้นการ workshop ในครั้งนี้ เราจะเรียนรู้วิธีการทำ data pipeline โดยใช้ Apache Airflow ซึ่งจะเริ่มต้นตั้งแต่การสอนพื้นฐานของภาษา Python ซึ่งเป็นภาษาหลักสำหรับการพัฒนา DAG เพื่อรันบน Airflow นั่นเอง

ในการ workshop ครั้งนี้เราจะรับ Airflow โดยใช้ Docker ซึ่ง resource ที่จัดเตรียมให้ในครั้งนี้อาจไม่เหมาะกับการนำไปใช้จริง (production) หากท่านใดที่ต้องการศึกษาเรียนรู้เพิ่มเติมสามารถเข้าไปดูได้ที่ https://airflow.apache.org/ ครับ

# สิ่งที่จำเป็น

สำหรับสิ่งที่จะต้องเตรียมเพื่อใช้สำหรับการ workshop จะต้องติดตั้งโปรแกรมดังนี้ โดยหากใครที่มีโปรแกรมอื่น ๆ ที่มีความสามารถเหมือนกัน ก็สามารถใช้ทดแทนกันได้ครับ

- Docker สำหรับใช้ติดตั้ง Apache Airflow [สามารถดาวโหลดได้ที่นี่](https://docs.docker.com/get-docker/)
- Visual Studio Code สำหรับใช้เขียนโค้ด [สามารถดาวโหลดได้ที่นี่](https://code.visualstudio.com/download)

# มาเริ่มต้นกันเลย

สำหรับคนที่คุ้นเคยภาษาอังกฤษและอยากได้ความรู้แน่น ๆ สำหรับการนำไปปรับใช้งานจริง (production) สามารถเข้าไปอ่าน document ของ Airflow [ได้ที่นี่](https://airflow.apache.org/docs/apache-airflow/stable/index.html)

สำหรับคนที่ดาวโหลด repository นี้ลงมาที่เครื่องแล้ว.ให้เข้าไปที่ folder `WUNCA-WORKSHOP-AIRFLOW` ทำตาม step ต่อจากนี้ได้เลย

## รัน Airflow บน Docker
- สร้าง folder ชื่อ dags, logs และ plugins สำหรับ Linux/MacOS สามารถใช้คำสั่งด้านล่างได้เลย

    ```bash
    mkdir -p ./dags ./logs ./plugins
    ```

- สำหรับ Linux/MacOS ให้รันคำสั่งด้านล่างนี้

    ```bash
    echo -e "AIRFLOW_UID=$(id -u)" > .env
    ```

- สร้างฐานข้อมูลและสร้าง user account สำหรับใช้งาน Airflow ให้รันคำสั่ง

    ```bash
    docker compose up airflow-init
    ```

- เริ่มต้นใช้งาน Airflow

    ```bash
    docker compose up -d
    ```

- เปลี่ยน password ของ mysql และสร้าง user เพื่อให้สามารถ login จาก host ใด ๆ ได้ (default จะให้ login จาก localhost เท่านั้น)

    ดู root password ที่ระบบ generated ให้ และ login เข้าสู่ mysql
    ```bash
    docker logs <container_name> 2>&1 | grep GENERATED
    
    docker exec -it <container_name> mysql -uroot -p
    ```

    รัน sql เพื่อเปลี่ยน password และสร้าง user root ให้สามารถ login จาก host ใด ๆ
    ```sql
    ALTER USER 'root'@'localhost' IDENTIFIED BY '<desired_password>';

    CREATE USER 'root'@'%' IDENTIFIED BY '<desired_password>'; GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
    ```

เมื่อทำตามขั้นตอนด้านบนแล้วสามารถเข้าใช้งาน Airflow ได้ที่ `http://localhost:8080` โดย username สำหรับ login ใช้งานนั้นจะใช้เป็น `airflow` และ password `airflow` หรือที่กำหนดไว้ในไฟล์ `docker-compose.yaml`

กรณีที่ต้องการลบ container และ volume ที่เกี่ยวข้องทั้งหมดสามารถใช้คำสั่ง `docker compose down --volumes --rmi all`

รายละเอียดอื่น ๆ สำหรับการ workshop ในครั้งนี้ สามารถดูได้จากไฟล์ ppt ที่อยู่ใน folder `resources` ครับ

ขอบคุณครับ