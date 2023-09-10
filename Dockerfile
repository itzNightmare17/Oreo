# Oreo - UserBot

FROM itznightmare17/oreo:main

# set timezone
ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY installer.sh .

RUN bash installer.sh

# changing workdir
WORKDIR "/root/itznightmare17"

# start the bot.
CMD ["bash", "startup"]
