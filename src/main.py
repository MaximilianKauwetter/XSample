import pandas as pd
import yfinance as yf
from flask import Flask, request, jsonify
from flask_caching import Cache

# --- App Initialization ---
app = Flask(__name__)
app.config.from_mapping(
    {
        "CACHE_TYPE": "SimpleCache",
        "CACHE_DEFAULT_TIMEOUT": 300,  # Cache timeout in seconds (5 minutes)
    }
)
cache = Cache(app)


# --- API Endpoint ---
@app.route("/api/stats", methods=["GET"])
@cache.cached(timeout=300, query_string=True)  # Cache based on URL query parameters
def get_stock_stats():
    """
    Provides key statistics for a given stock ticker over a specified time range.
    ---
    Query Parameters:
      - ticker (str): Required. The stock ticker symbol (e.g., 'MSFT').
      - start (str): Optional. Start date in 'YYYY-MM-DD' format.
      - end (str): Optional. End date in 'YYYY-MM-DD' format.
    ---
    Returns:
      - JSON response with statistics or an error message.
    """
    # 1. Get query parameters from the request URL
    ticker_symbol = request.args.get("ticker")
    start_date = request.args.get("start")
    end_date = request.args.get("end")
    print(f"Request: {ticker_symbol}, {start_date}, {end_date}")

    # 2. Validate that the 'ticker' parameter was provided
    if not ticker_symbol:
        print("Invalid ticker symbol provided.")
        return jsonify({"error": "Ticker symbol is a required parameter."}), 400

    try:
        # 3. Fetch historical data from yfinance
        stock_data: pd.DataFrame = yf.download(
            ticker_symbol,
            start=start_date,
            end=end_date,
            progress=False,
            multi_level_index=False,
            auto_adjust=False,
        )

        if stock_data is None or stock_data.empty:
            return (
                jsonify(
                    {
                        "error": f"No data found for ticker '{ticker_symbol}'. It might be an invalid symbol or delisted."
                    }
                ),
                404,
            )

        # Ensure data is sorted by date to get the correct 'last_close'
        stock_data.sort_index(ascending=True, inplace=True)

        # 4. Calculate key statistics
        period_high = stock_data["High"].max()
        period_low = stock_data["Low"].min()
        average_price = stock_data["Close"].mean()
        last_close = stock_data["Close"].iloc[-1]  # .iloc[-1] gets the last item

        # 5. Structure the response
        response = {
            "period_high": round(period_high, 2),
            "period_low": round(period_low, 2),
            "average_close_price": round(average_price, 2),
            "last_close_price": round(last_close, 2),
        }
        print(f"Successfully response: {response}")
        return jsonify(response)

    except Exception as e:
        # Generic error handler for other potential issues (e.g., network problems)
        print("Error")
        return (
            jsonify({"error": "An unexpected error occurred.", "details": str(e)}),
            500,
        )


# --- Main execution ---
if __name__ == "__main__":
    # Runs the Flask app on localhost, port 5000
    # Set debug=False for production environments
    print("Start app")
    app.run(debug=False)
