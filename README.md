# Project Setup Instructions

This project has 5 services as mentioned below:
1. **account_svc_rest** - Implements rest APIs for various account related functionalities
2. **account_svc_grpc** - Implements grpc server for fetching the account statement
3. **pdf_generation_svc** - Implements pdf generation logic for the account statement
4. **notification_svc_1** - Consumes messages for the account creation events
5. **notification_svc_2** - Consumes messages for the account creation as well as pdf generated events


## Pre-requisites

### 1. Clone the Repository

```
git clone git@github.com:anantvardhan04/svc_middleware_assignment.git && cd svc_middleware_assignment
```

## Setup the project and Run all the services

### 1. Do initial setup and run `account_svc_rest` service

1. Go to **account_svc_rest** directory and run below command:
```
cd account_svc_rest && sh bin/setup.sh
```
  
### 2. Run `account_svc_grpc` service

1. Open a new shell/terminal
2. Go to **account_svc_grpc** directory and run below command:
```
cd account_svc_grpc && sh bin/setup.sh
```

### 3. Run `pdf_generation` service

1. Open a new shell/terminal
2. Go to **pdf_generation_svc** directory and run below command:
```
cd pdf_generation_svc && sh bin/setup.sh
```

### 4. Run `notification service 1`

1. Open a new shell/terminal
2. Go to **notification_svc_1** directory and run below command:
```
cd notification_svc_1 && sh bin/setup.sh
```

### 5. Run `notification service 2`

1. Open a new shell/terminal
2. Go to **notification_svc_2** directory and run below command:
```
cd notification_svc_2 && sh bin/setup.sh
```


##  **Verify the Setup**

### 1. Create a customer  account

1. Open a new terminal
```
curl -X POST http://127.0.0.1:5000/account/create -d '{"name": "Manish Kumar", "phone_number": "8873186985", "account_type": "Savings"}' -H "Content-Type: application/json"
```

### 2. Fetch Customer Details

```
curl http://127.0.0.1:5000/account/1
```

### 3. Fetch Account Statement for a customer

```
curl http://127.0.0.1:5000/account/statement/1
```

### 4. Generate PDF for Account Statement for a customer

```
curl http://127.0.0.1:5000/account/statement/1/generatepdf
```

After running the above curl, go inside **pdf_generation_svc/statements** directory to access the generated pdf.
