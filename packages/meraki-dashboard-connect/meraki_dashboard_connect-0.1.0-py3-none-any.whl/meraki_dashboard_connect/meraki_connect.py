import meraki
import meraki_env
import sys


def dashboard_connection():
    api_key = meraki_env.api_key()
    base_url = meraki_env.base_url()
    # instance api meraki_sd
    try:
        d = meraki.DashboardAPI(api_key=api_key,
                                # base_url='https://api-mp.meraki.com/api/v1/',
                                base_url=base_url,
                                # log_file_prefix="",
                                print_console=False,
                                output_log=False,  
                                maximum_retries = 50,
                                nginx_429_retry_wait_time = 2
                                # retry_4xx_error=True
                                )
    except meraki.APIError as e:
        print(f'Meraki API error: {e}')
        print(f'status code = {e.status}')
        print(f'reason = {e.reason}')
        print(f'error = {e.message}')
        sys.exit(1)
    except Exception as e:
        print(f'some other error: {e}')
        sys.exit(1)

    return d
