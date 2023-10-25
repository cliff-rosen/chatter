const prod = {
  url: {
    //API_URL: "https://api-staging.trippersalmanac.com",
    //API_URL: "http://app-dm-02.eba-kv6ia4sm.us-east-1.elasticbeanstalk.com/"
    API_URL: "https://dosemerx-api.ironcliff.ai"
  },
};

const dev = {
  url: {
    API_URL: "http://127.0.0.1:5000",
    //API_URL: "http://xogene-01.eba-zdq22h3k.us-east-1.elasticbeanstalk.com",
  },
};

export const config = process.env.NODE_ENV === "development" ? dev : prod;
