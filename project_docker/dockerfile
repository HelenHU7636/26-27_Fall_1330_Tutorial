FROM python:3.13-slim-bookworm@sha256:ed86c82274b3c69b52fb5820f358f0bd7df0b603332063cb5c6e32bd220c3e6e
ENV COURSE_ENVIRONMENT_VERSION=2026-v03
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 TERM=xterm-256color COLUMNS=80 LINES=24
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash bash-completion nano vim git curl ca-certificates less tree unzip zip procps \
    ncurses-bin ripgrep file jq \
    && rm -rf /var/lib/apt/lists/*
RUN printf '%s\n' '. /usr/share/bash-completion/bash_completion' >> /etc/bash.bashrc
COPY vimrc /etc/vim/vimrc
RUN useradd --create-home --uid 1000 --shell /bin/bash student
COPY entrypoint.sh /usr/local/bin/course_entrypoint
RUN chmod 755 /usr/local/bin/course_entrypoint
COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt && python -m pip check
WORKDIR /workspace
USER student
ENTRYPOINT ["/usr/local/bin/course_entrypoint"]
CMD ["python", "tic_tac_toe.py"]
