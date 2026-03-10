FROM python

WORKDIR /usr/src/apps

COPY ./ /usr/src/apps

ENV FLASK_APP=app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod u+x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]