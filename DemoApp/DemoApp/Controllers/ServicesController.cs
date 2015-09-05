using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;
using System.Text;
using RestSharp;
using Newtonsoft.Json.Linq;
using System.Xml;
using System.Threading.Tasks;
using DemoApp.Models;
using System.Xml.Schema;
using Newtonsoft.Json;
using System.Collections.Specialized;

namespace DemoApp.Controllers
{
    public class ServicesController : ApiController, IDisposable
    {
        public string serviceConfig;
        XmlDocument xmlDoc;
        XmlNode rootNode;
        XmlNode serviceNode;
        XmlNode apiKeysNode;

        public ServicesController()
        {
            xmlDoc = new XmlDocument();
            xmlDoc.Load(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Configs/ServiceConfig.xml"));
            rootNode = xmlDoc.SelectSingleNode("ServiceConfig");
            serviceNode = xmlDoc.SelectSingleNode("ServiceConfig/Service");
            apiKeysNode = xmlDoc.SelectSingleNode("ServiceConfig/ApiKeys");
            
        }

        // GET api/values/5
        public List<string> GetApiDetails(string serviceName = "Practo", string apiName = "doctors")
        {
            XmlNodeList matches = xmlDoc.SelectNodes("ServiceConfig/Service[@Name='" + serviceName + "']/Api[@Name='" + apiName + "']/Parameters");
            List<String> allParameters = (from XmlNode item in matches
                                         select item.InnerText.ToString()).ToList();

            return allParameters;
        }       

        // POST api/valuesx
        public async Task<JObject> GetServiceDetails(string serviceName = "Google", string apiName = "nearbySearch", string parameters = "location=12.9209839,77.610254&radius=500&types=food")  
        {
            XmlNodeList matches = xmlDoc.SelectNodes("ServiceConfig/Service[@Name='"+ serviceName + "']/Api[@Name='"+ apiName +"']");
            string baseUrl= xmlDoc.SelectSingleNode("ServiceConfig/Service[@Name='" + serviceName + "']").Attributes["Url"].Value;
            var resourceUrl = matches.Item(0).Attributes["Url"].Value;

            Console.WriteLine(serviceName +  "   " + apiName +  "   "  +parameters);

            JObject s = await GetResponseFromApi(baseUrl, resourceUrl, serviceName, parameters);            
            return s;
        }


        // Get the response from Api
        private async Task<JObject> GetResponseFromApi(string baseUrl, string url, string serviceName, string paramenters)
        {
            string responseData;
            string responseUrl;

            XmlNodeList matches = xmlDoc.SelectNodes("ServiceConfig/ApiKeys/Key[@name='" + serviceName + "']");
            Dictionary<string, string> apiKeys = new Dictionary<string, string>();
            if (matches != null && matches.Count > 0)
            {
                IEnumerable<XmlNode> allParameters = (from XmlNode item in matches.Item(0).ChildNodes
                                                      select item);
                apiKeys = new Dictionary<string, string>();
                foreach (var item in allParameters)
                {
                    apiKeys.Add(item.Name, item.InnerText);
                }   
            }
            

            var baseAddress = new Uri(baseUrl);
            
            if (baseUrl.Contains('?'))
            {
                var v = baseUrl.Substring(baseUrl.IndexOf('?'));
                v = string.IsNullOrEmpty(v) ? v : v + "&";
                responseUrl = v.Length != 0 ? (url + v + paramenters) : (url + paramenters);
            }
            else
            {
                responseUrl = url + paramenters;
            }
            

            using (var httpClient = new HttpClient { BaseAddress = baseAddress })
            {
                if (matches != null && matches.Count > 0)
                {
                    foreach (var akey in apiKeys)
                    {
                        httpClient.DefaultRequestHeaders.TryAddWithoutValidation(akey.Key, akey.Value);
                    } 
                }

                using (var response = await httpClient.GetAsync(responseUrl))
                {

                    responseData = await response.Content.ReadAsStringAsync();
                }
            }
            JObject obj = JObject.Parse(responseData);

            return obj;
        }

        public string GetReponseFromApis()
        {
            // Create a request for the URL. 
            WebRequest request = WebRequest.Create("https://api.practo.com/doctors/?page=1");
            request.Headers.Add("X-CLIENT-ID", "e35afaf5-ff2d-4f66-b735-7d7b89604843");
            request.Headers.Add("X-API-KEY", "mHdhUVBar2TTquzJklpcmUwJ5Oo");

            // Get the response.
            WebResponse response = request.GetResponse();
            
            // Get the stream containing content returned by the server.
            Stream dataStream = response.GetResponseStream();

            // Open the stream using a StreamReader for easy access.
            StreamReader reader = new StreamReader(dataStream);
                
            // Read the content.
            string responseFromServer = reader.ReadToEnd();

            // Clean up the streams and the response.
            reader.Close();
            response.Close();
            return responseFromServer;
        }

        [HttpPost]
        public HttpResponse AddApi(JObject service)
        {
            XmlNode node = xmlDoc.SelectSingleNode("ServiceConfig/Service[@Name=" + service["provider"].ToString() + "]/Api");
            XmlNode keyNode = xmlDoc.SelectSingleNode("ServiceConfig/ApiKeys/Key[@Name=" + service["provider"].ToString() + "]");
            
            if (node != null)
            {
                serviceNode.RemoveChild(node);
            }

            if (keyNode != null)
            {
                apiKeysNode.RemoveChild(keyNode);     
            }
            
            // Key
            XmlNode newKeyNode = xmlDoc.CreateNode(XmlNodeType.Element, "Key", xmlDoc.DocumentElement.NamespaceURI);
            var jHeaders = service["headers"] as JObject;
            var headers = jHeaders.ToObject<Dictionary<string, string>>();
            foreach (var header in headers)
            {
                    
                XmlElement hName = xmlDoc.CreateElement(header.Key);
                hName.InnerText = header.Value;

                newKeyNode.AppendChild(hName);                    
            }

            // Service
            XmlNode newService = xmlDoc.CreateNode(XmlNodeType.Element, "Service", xmlDoc.DocumentElement.NamespaceURI);
            XmlAttribute newServiceName = xmlDoc.CreateAttribute("Name"); 
            newServiceName.Value = service["provider"].ToString();
            XmlAttribute newServiceEndpoint = xmlDoc.CreateAttribute("Url");
            newServiceEndpoint.Value = service["endpoint"].ToString();

            newService.Attributes.Append(newServiceName);
            newService.Attributes.Append(newServiceEndpoint);

            // Apis
            XmlNode newApi = xmlDoc.CreateNode(XmlNodeType.Element, "Api", xmlDoc.DocumentElement.NamespaceURI);
            foreach (var item in service["apis"])
            {
                var jApis = item.ToObject<Apis>();
                    
                XmlAttribute newApiName = xmlDoc.CreateAttribute("Name");
                newApiName.Value = item["name"].ToString();
                XmlAttribute newApiResourceUrl = xmlDoc.CreateAttribute("Url");
                newApiResourceUrl.Value = item["resourceUrl"].ToString();
                newApi.Attributes.Append(newApiName);
                newApi.Attributes.Append(newApiResourceUrl);


                foreach (var para in item["parameters"])
                {
                    XmlElement par = xmlDoc.CreateElement("Parameters");
                    par.InnerText = para.ToString();
                    newApi.AppendChild(par);
                }
            }

            newService.AppendChild(newApi);
            rootNode.AppendChild(newService);
            apiKeysNode.AppendChild(newKeyNode);

            xmlDoc.Save(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Configs/ServiceConfig.xml")); 
            

            return new HttpResponse();
        }

        [HttpGet]
        public HttpResponse DeleteService(string serviceName)
        {
            XmlNode serviceNode = xmlDoc.SelectSingleNode("ServiceConfig/Service[@Name='" + serviceName  + "']");
            XmlNode keyNode = xmlDoc.SelectSingleNode("ServiceConfig/ApiKeys/Key[@Name='" + serviceName + "']");

            if (serviceNode != null)
            {
                serviceNode.ParentNode.RemoveChild(serviceNode);                
            }

            if (keyNode != null)
            {
                apiKeysNode.RemoveChild(keyNode);
            }

            xmlDoc.Save(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Configs/ServiceConfig.xml")); 

            var res = new HttpResponse();
            res.StatusCode = HttpStatusCode.OK;
            return res; ;
        }

        [HttpGet]
        public List<string> ListServices()
        {
            XmlNodeList serviceNode = xmlDoc.SelectNodes("ServiceConfig/Service");


            List<String> allServices = new List<string>();
            foreach ( XmlNode item in serviceNode)
            {
                allServices.Add(item.Attributes["Name"].Value);
            }

            return allServices;
        }

        public void Dispose()
        {
            GC.Collect();
            GC.WaitForPendingFinalizers();
        }
    }
}