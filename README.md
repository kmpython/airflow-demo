# airflow-demo-dag

In this repository, I have made a simple Airflow dag to learn the fundamentals of working with Airflow. I Installed airflow on EC2 - Ubuntu
and configured airflow to work with MySQL backend


DAG has the following features:
- File sensor on S3 bucket
- XCOM variable
- Variables passed from Admin Screen
- Branching

### Adding AWS credentials for file sensor using boto3

1. create a `.aws` folder in home directory
2. create a file called `credentials`
3. add the following information in the file
    ```
    [default]
    aws_access_key_id=[AWS_ACCESS_KEY]
    aws_secret_access_key=[AWS_SECRET_KEY]
    ```
  
### Passing variables from the UI to the DAG

In the airflow console webpage
1. Click on ADMIN
2. Click on Variables
3. Add your variables
    * In my demo, I have added variables called s3_bucket, s3_file, s3_file_trigger
4. pull them into the program using
    ```
    from airflow.models import DAG, Variable
    s3_bucket = Variable.get("s3_bucket")             
    s3_file = Variable.get("s3_file")                   
    s3_file_trigger = Variable.get("s3-file-trigger")   
    ```
    
### Setting up my-sql backend

#### Installing MySQL
By default, airflow backend comes with a Sqlite database. Sqlite db works well for small tests and poc projects but for prodution we need a more robust database. Also, Sqlite db does not support parallel processing, we will need to change the database to unlock parallel processing capabilites 
```
sudo apt-get updae
sudo apt install mysql-server
```
 
#### Configure MySQL
perform the security setup as required needed

I have created a new user called `airflow-user` which I will use to access the database  
I also created a database called airflow  

If we come across an error -  
`Exception: Global variable explicit_defaults_for_timestamp needs to be on (1) for mysql`   
while executing `airflow initdb` command then we will need to set
`set global explicit_defaults_for_timestamp = 1;` 
on our instance of mysql

[refer here for more details about the error](https://stackoverflow.com/questions/15701636/how-to-enable-explicit-defaults-for-timestamp/40886460)

#### Install python modules to talk to airflow
to configure airflow to use our mysql database we will need to install the drivers/modules so that python can connect with the database  
NOTE:if you are using python3, we will need to install `mysqlclient` instead of `MySqldb` as MySQLdb is not supported in Python3.x  
[click here for reference]

```
# we will need to install prerequsities first
sudo apt-get install libmysqlclient-dev

# install mysql client
sudo pip3 install mysqlclient
```

#### Configure airflow
we will need to change the connection strings in the airflow.cfg file

```
sql_alchemy_conn = mysql://airflow-user:your-password@localhost:3306/airflow
executor = LocalExecutor
```

references:
*  https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04
*  https://stackoverflow.com/questions/7475223/mysql-config-not-found-when-installing-mysqldb-python-interface
*  http://site.clairvoyantsoft.com/installing-and-configuring-apache-airflow/
