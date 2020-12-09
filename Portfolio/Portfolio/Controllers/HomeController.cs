using System;
using System.Net;
using System.Threading.Tasks;
using System.Web.Mvc;
using log4net;
using Portfolio.Extensions;
using Portfolio.Models;
using RestSharp;

namespace Portfolio.Controllers
{
   public class HomeController : Controller
   {
      private readonly ILog _logger = LogManager.GetLogger(typeof(HomeController));

      public ActionResult Index()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Index));

         return View();
      }

      public ActionResult About()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(About));

         return View();
      }

      [HttpGet]
      public ActionResult Contact()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Contact));

         return View();
      }

      [HttpPost]
      public async Task<ActionResult> Contact(Models.EmailMessage emailMessage)
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Contact));

         ViewBag.Message = "Message Failed";

         if (ModelState.IsValid)
         {
            if (!string.IsNullOrEmpty(emailMessage.FromAddress) && !string.IsNullOrEmpty(emailMessage.MessageContent))
            {
               // Get the secret key value from 
               string appKey = Environment.GetEnvironmentVariable("AGameFunctionAppKey");

               emailMessage.Subject = "Contact Form: mbcarey.com";

               RestClient client = new RestClient(Settings.Default.AGameWebUrl);
               RestRequest request = new RestRequest($"api/PersonalEmail?code={appKey}", Method.POST, DataFormat.Json);
               request.AddJsonBody(await emailMessage.ToJsonAsync());
               IRestResponse response = await client.ExecuteAsync(request);

               if (response.StatusCode == HttpStatusCode.OK)
               {
                  ViewBag.Message = "Message Sent";
               }
            }
         }

         ModelState.Clear();

         return View();
      }

      public ActionResult Git()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Git));

         return View();
      }
   }
}