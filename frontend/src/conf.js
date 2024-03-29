const prod = {
  url: {
    API_URL: "https://dosemerx-api.ironcliff.ai"
  },
};

const dev = {
  url: {
    API_URL: "http://127.0.0.1:5000"
  },
};

export const config = process.env.NODE_ENV === "development" ? dev : prod;
