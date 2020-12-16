using System;
using System.Reflection;
using System.Web.Mvc;
using System.Web.Optimization;
using System.Web.Routing;
using hbehr.recaptcha;
using log4net;

namespace Portfolio
{
	public class MvcApplication : System.Web.HttpApplication
   {
      private static readonly ILog _logger = LogManager.GetLogger(typeof(MvcApplication));

      protected void Application_Start()
      {
         string l4Net = Server.MapPath("~/web.config");
         log4net.Config.XmlConfigurator.ConfigureAndWatch(new System.IO.FileInfo(l4Net));

         // Check to see what logging levels are active
         _logger.Info("Application Start - Info Logging level Check");
         _logger.Warn("Application Start - Warn Logging level Check");
         _logger.Error("Application Start - Error Logging level Check");
         _logger.Fatal("Application Start - Fatal Logging level Check");
         _logger.Debug("Application Start - Debug Logging level Check");

         _logger.Info($"Version: {Assembly.GetExecutingAssembly().GetName()}");

         // Configure and activate the ReCaptcha code in the application
         string reCaptchaPublic = Environment.GetEnvironmentVariable("ReCaptchaPublic");
         string reCaptchaSecret = Environment.GetEnvironmentVariable("ReCaptchaSecret");
         
#if DEBUG
         if (string.IsNullOrEmpty(reCaptchaPublic))
            reCaptchaPublic = Settings.Default.ReCaptchaPublic;
         
         if (string.IsNullOrEmpty(reCaptchaSecret))
            reCaptchaPublic = Settings.Default.ReCaptchaSecret;
#endif
         
         ReCaptcha.Configure(reCaptchaPublic, reCaptchaSecret);


         AreaRegistration.RegisterAllAreas();
			FilterConfig.RegisterGlobalFilters( GlobalFilters.Filters );
			RouteConfig.RegisterRoutes( RouteTable.Routes );
			BundleConfig.RegisterBundles( BundleTable.Bundles );
		}
	}
}
