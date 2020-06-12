// for configuring when hosting on aws. change public to the AWS IP

module.exports = {
  devServer: {
    disableHostCheck: true,
    public: ""
  }
};
