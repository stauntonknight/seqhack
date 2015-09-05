using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using YAXLib;

namespace DemoApp.Configs
{
    public class Person
    {
        public string SSN { get; set; }
        public string Name { get; set; }
        public string Family { get; set; }
        public int Age { get; set; }
    }    

    public class ServiceConfig
    {
        [YAXAttributeForClass]
        public string Name { get; set; }


        
    }
}