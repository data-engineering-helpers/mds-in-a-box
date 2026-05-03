#!/usr/bin/env python

try:
    from .merge_customer_common import run_customer_merge_job
except ImportError:
    from merge_customer_common import run_customer_merge_job


def main(argv: list[str] | None = None) -> None:
    run_customer_merge_job(job_name="merge_customer_001_simple", argv=argv)


if __name__ == "__main__":
    main()

