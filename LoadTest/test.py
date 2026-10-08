# import asyncio
# import aiohttp
# import time
# import statistics


# # ==========================================
# # SETTINGS
# # ==========================================

# TOTAL_REQUESTS = 100000

# MAX_CONCURRENT_REQUESTS = 100

# TIMEOUT_SECONDS = 30


# # ==========================================
# # GLOBAL STATISTICS
# # ==========================================

# total_sent = 0
# successful = 0
# failed = 0

# response_times = []

# lock = asyncio.Lock()


# # ==========================================
# # SEND ONE REQUEST
# # ==========================================

# async def send_request(session, url):

#     global total_sent
#     global successful
#     global failed

#     start_time = time.perf_counter()

#     try:

#         async with session.get(url) as response:

#             await response.read()

#             end_time = time.perf_counter()

#             response_time = end_time - start_time

#             async with lock:

#                 total_sent += 1

#                 response_times.append(
#                     response_time
#                 )

#                 if 200 <= response.status < 300:

#                     successful += 1

#                 else:

#                     failed += 1

#     except Exception:

#         async with lock:

#             total_sent += 1
#             failed += 1


# # ==========================================
# # SEND REQUESTS FOR ONE STAGE
# # ==========================================

# async def run_stage(
#     session,
#     url,
#     duration_seconds,
#     requests_per_minute
# ):

#     print()
#     print("------------------------------------------")
#     print(
#         f"Running {requests_per_minute:,} "
#         f"requests/minute"
#     )
#     print(
#         f"Duration: {duration_seconds} seconds"
#     )
#     print("------------------------------------------")

#     requests_per_second = (
#         requests_per_minute / 60
#     )

#     delay = 1 / requests_per_second

#     stage_start = time.perf_counter()

#     tasks = []

#     while (
#         time.perf_counter() - stage_start
#         < duration_seconds
#     ):

#         if total_sent >= TOTAL_REQUESTS:

#             break

#         task = asyncio.create_task(
#             send_request(
#                 session,
#                 url
#             )
#         )

#         tasks.append(task)

#         if len(tasks) >= MAX_CONCURRENT_REQUESTS:

#             done, pending = await asyncio.wait(
#                 tasks,
#                 return_when=asyncio.FIRST_COMPLETED
#             )

#             tasks = list(pending)

#         await asyncio.sleep(delay)

#     if tasks:

#         await asyncio.gather(
#             *tasks,
#             return_exceptions=True
#         )


# # ==========================================
# # MAIN
# # ==========================================

# async def main():

#     print()
#     print("==========================================")
#     print("   EMPLOYEE EVENT REGISTRATION")
#     print("          LOAD TEST")
#     print("==========================================")

#     # --------------------------------------
#     # GET TARGET URL
#     # --------------------------------------

#     url = input(
#         "\nEnter target URL: "
#     ).strip()

#     print()
#     print("Target URL:")
#     print(url)

#     print()
#     print(
#         f"Maximum requests: {TOTAL_REQUESTS:,}"
#     )

#     input(
#         "\nPress ENTER to start the test..."
#     )

#     # --------------------------------------
#     # HTTP CLIENT
#     # --------------------------------------

#     connector = aiohttp.TCPConnector(
#         limit=MAX_CONCURRENT_REQUESTS
#     )

#     timeout = aiohttp.ClientTimeout(
#         total=TIMEOUT_SECONDS
#     )

#     # --------------------------------------
#     # START SESSION
#     # --------------------------------------

#     async with aiohttp.ClientSession(
#         connector=connector,
#         timeout=timeout
#     ) as session:

#         test_start = time.perf_counter()

#         # ----------------------------------
#         # LOAD STAGES
#         # ----------------------------------
#         stages = [

#     # duration, requests per minute

#     (60, 100000),
# ]

#         # ----------------------------------
#         # RUN STAGES
#         # ----------------------------------

#         for duration, rpm in stages:

#             if total_sent >= TOTAL_REQUESTS:

#                 break

#             await run_stage(
#                 session,
#                 url,
#                 duration,
#                 rpm
#             )

#             print()
#             print(
#                 f"Total sent: {total_sent:,}"
#             )

#             print(
#                 f"Successful: {successful:,}"
#             )

#             print(
#                 f"Failed: {failed:,}"
#             )

#     # ======================================
#     # FINAL REPORT
#     # ======================================

#     total_time = (
#         time.perf_counter()
#         - test_start
#     )

#     print()
#     print("==========================================")
#     print("             TEST COMPLETE")
#     print("==========================================")

#     print(
#         f"Total requests : {total_sent:,}"
#     )

#     print(
#         f"Successful     : {successful:,}"
#     )

#     print(
#         f"Failed         : {failed:,}"
#     )

#     if response_times:

#         average = statistics.mean(
#             response_times
#         )

#         minimum = min(
#             response_times
#         )

#         maximum = max(
#             response_times
#         )

#         print()
#         print(
#             f"Average response : "
#             f"{average:.3f} seconds"
#         )

#         print(
#             f"Minimum response : "
#             f"{minimum:.3f} seconds"
#         )

#         print(
#             f"Maximum response : "
#             f"{maximum:.3f} seconds"
#         )

#     print()
#     print(
#         f"Total test time: "
#         f"{total_time:.2f} seconds"
#     )

#     if total_time > 0:

#         rps = (
#             total_sent / total_time
#         )

#         print(
#             f"Actual RPS: {rps:.2f}"
#         )


# # ==========================================
# # START PROGRAM
# # ==========================================

# if __name__ == "__main__":

#     asyncio.run(main())





















import asyncio
import aiohttp
import time
import csv
from collections import Counter


# ============================================================
# CONFIGURATION
# ============================================================

TEST_DURATION_MINUTES = 20

MAX_CONCURRENT_REQUESTS = 200

REQUEST_TIMEOUT = 30


# ============================================================
# LOAD PROFILE
#
# duration in seconds
# target requests per minute
# ============================================================

LOAD_STAGES = [

    (120, 1_000),       # 0 - 2 min

    (120, 5_000),       # 2 - 4 min

    (180, 10_000),      # 4 - 7 min

    (180, 25_000),      # 7 - 10 min

    (180, 50_000),      # 10 - 13 min

    (180, 75_000),      # 13 - 16 min

    (240, 100_000),     # 16 - 20 min
]


# ============================================================
# STATISTICS
# ============================================================

total_requests = 0
successful_requests = 0
failed_requests = 0

response_times = []

status_codes = Counter()

errors = Counter()

lock = asyncio.Lock()


# ============================================================
# SEND ONE REQUEST
# ============================================================

async def send_request(session, url):

    global total_requests
    global successful_requests
    global failed_requests

    start_time = time.perf_counter()

    try:

        async with session.get(url) as response:

            await response.read()

            end_time = time.perf_counter()

            response_time = (
                end_time - start_time
            )

            async with lock:

                total_requests += 1

                response_times.append(
                    response_time
                )

                status_codes[
                    response.status
                ] += 1

                if 200 <= response.status < 300:

                    successful_requests += 1

                else:

                    failed_requests += 1

    except Exception as error:

        end_time = time.perf_counter()

        response_time = (
            end_time - start_time
        )

        async with lock:

            total_requests += 1

            response_times.append(
                response_time
            )

            failed_requests += 1

            errors[
                type(error).__name__
            ] += 1


# ============================================================
# RUN ONE LOAD STAGE
# ============================================================

async def run_stage(
    session,
    url,
    duration,
    requests_per_minute
):

    print()
    print("=" * 60)

    print(
        f"LOAD: {requests_per_minute:,} requests/minute"
    )

    print(
        f"DURATION: {duration} seconds"
    )

    print("=" * 60)

    requests_per_second = (
        requests_per_minute / 60
    )

    delay = (
        1 / requests_per_second
    )

    stage_start = time.perf_counter()

    tasks = []

    while True:

        elapsed = (
            time.perf_counter()
            - stage_start
        )

        if elapsed >= duration:

            break

        task = asyncio.create_task(
            send_request(
                session,
                url
            )
        )

        tasks.append(task)

        if len(tasks) >= MAX_CONCURRENT_REQUESTS:

            done, pending = await asyncio.wait(
                tasks,
                return_when=asyncio.FIRST_COMPLETED
            )

            tasks = list(pending)

        await asyncio.sleep(delay)

    if tasks:

        await asyncio.gather(
            *tasks,
            return_exceptions=True
        )

    print()

    print(
        f"Requests completed: {total_requests:,}"
    )

    print(
        f"Successful: {successful_requests:,}"
    )

    print(
        f"Failed: {failed_requests:,}"
    )


# ============================================================
# SAVE CSV REPORT
# ============================================================

def save_report():

    filename = "load_test_report.csv"

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Metric",
            "Value"
        ])

        writer.writerow([
            "Total Requests",
            total_requests
        ])

        writer.writerow([
            "Successful Requests",
            successful_requests
        ])

        writer.writerow([
            "Failed Requests",
            failed_requests
        ])

        if total_requests > 0:

            failure_percentage = (
                failed_requests
                / total_requests
                * 100
            )

            writer.writerow([
                "Failure Percentage",
                f"{failure_percentage:.2f}%"
            ])

        if response_times:

            average = (
                sum(response_times)
                / len(response_times)
            )

            minimum = min(
                response_times
            )

            maximum = max(
                response_times
            )

            writer.writerow([
                "Average Response Time",
                f"{average:.4f} seconds"
            ])

            writer.writerow([
                "Minimum Response Time",
                f"{minimum:.4f} seconds"
            ])

            writer.writerow([
                "Maximum Response Time",
                f"{maximum:.4f} seconds"
            ])

        writer.writerow([])

        writer.writerow([
            "HTTP Status Code",
            "Count"
        ])

        for status, count in sorted(
            status_codes.items()
        ):

            writer.writerow([
                status,
                count
            ])

        writer.writerow([])

        writer.writerow([
            "Error Type",
            "Count"
        ])

        for error, count in errors.items():

            writer.writerow([
                error,
                count
            ])

    return filename


# ============================================================
# MAIN PROGRAM
# ============================================================

async def main():

    global total_requests

    print()
    print("=" * 60)

    print(
        "      EMPLOYEE EVENT REGISTRATION"
    )

    print(
        "             LOAD TEST"
    )

    print("=" * 60)

    print()

    # --------------------------------------------------------
    # TARGET URL
    # --------------------------------------------------------

    url = input(
        "Enter target URL: "
    ).strip()

    print()

    print(
        f"Target URL: {url}"
    )

    print(
        f"Test duration: {TEST_DURATION_MINUTES} minutes"
    )

    print(
        "Load starts at 1,000 RPM"
    )

    print(
        "Load increases up to 100,000 RPM"
    )

    print()

    input(
        "Press ENTER to start the load test..."
    )

    print()

    connector = aiohttp.TCPConnector(
        limit=MAX_CONCURRENT_REQUESTS
    )

    timeout = aiohttp.ClientTimeout(
        total=REQUEST_TIMEOUT
    )

    test_start = time.perf_counter()

    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout
    ) as session:

        # ----------------------------------------------------
        # RUN ALL LOAD STAGES
        # ----------------------------------------------------

        for duration, rpm in LOAD_STAGES:

            await run_stage(
                session,
                url,
                duration,
                rpm
            )

    # ========================================================
    # FINAL RESULTS
    # ========================================================

    total_time = (
        time.perf_counter()
        - test_start
    )

    print()
    print("=" * 60)

    print(
        "                 TEST COMPLETE"
    )

    print("=" * 60)

    print()

    print(
        f"Total Requests     : {total_requests:,}"
    )

    print(
        f"Successful Requests: {successful_requests:,}"
    )

    print(
        f"Failed Requests    : {failed_requests:,}"
    )

    if total_requests > 0:

        failure_percentage = (
            failed_requests
            / total_requests
            * 100
        )

        print(
            f"Failure Percentage : "
            f"{failure_percentage:.2f}%"
        )

    if response_times:

        average = (
            sum(response_times)
            / len(response_times)
        )

        minimum = min(
            response_times
        )

        maximum = max(
            response_times
        )

        print()

        print(
            f"Average Response Time: "
            f"{average:.4f} seconds"
        )

        print(
            f"Minimum Response Time: "
            f"{minimum:.4f} seconds"
        )

        print(
            f"Maximum Response Time: "
            f"{maximum:.4f} seconds"
        )

    print()

    print(
        f"Total Test Time: "
        f"{total_time:.2f} seconds"
    )

    if total_time > 0:

        actual_rps = (
            total_requests
            / total_time
        )

        print(
            f"Actual RPS: "
            f"{actual_rps:.2f}"
        )

    print()

    print("HTTP STATUS CODES:")

    for status, count in sorted(
        status_codes.items()
    ):

        print(
            f"  {status}: {count:,}"
        )

    if errors:

        print()

        print("ERRORS:")

        for error, count in errors.items():

            print(
                f"  {error}: {count:,}"
            )

    # --------------------------------------------------------
    # SAVE REPORT
    # --------------------------------------------------------

    report_file = save_report()

    print()

    print(
        f"Report saved as: {report_file}"
    )

    print()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        print()
        print(
            "Test manually stopped by user."
        )















