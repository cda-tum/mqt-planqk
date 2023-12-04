FROM ghcr.io/planqk/job-template:latest-base-1.0.0

ENV ENTRY_POINT app.user_code.src.program:run

COPY . ${USER_CODE_DIR}
RUN conda env update -n planqk --file ${USER_CODE_DIR}/environment.yml
