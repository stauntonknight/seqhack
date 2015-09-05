using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace DemoApp.Models
{
    public class Api
    {
        public string name { get; private set; }
        public List<string> parameters { get; private set; }
        public string resourceUrl { get; private set; }
    }

    public class Apis
    {
        public List<Api> apis { get; private set; }  
    }

    public class ClientModel
    {
        public string provider{ get; private set; }
        public string endpoint { get; private set; }
        public Dictionary<string, string> headers { get; private set; }
        public Api apis;
        
    }
}