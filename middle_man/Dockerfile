FROM python

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["sh", "-c", "trap 'exit' TERM; python downloadExcelSheet.py && python convertToPostgres.py; while true; do sleep 1; done"]