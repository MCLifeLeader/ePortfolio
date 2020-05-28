using System.Web.Mvc;
using log4net;

namespace Portfolio.Controllers
{
   public class ProjectsController : Controller
   {
      private readonly ILog _logger = LogManager.GetLogger(typeof(ProjectsController));

      public ActionResult Index()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Index));

         return View();
      }

      public ActionResult AdverTran()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(AdverTran));

         return View();
      }

      public ActionResult AGameEmpowerment()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(AGameEmpowerment));

         return View();
      }

      public ActionResult Cit261()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Cit261));

         return View();
      }

      public ActionResult Cs313()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Cs313));

         return View();
      }

      public ActionResult Cs364()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Cs364));

         return View();
      }

      public ActionResult Encompass()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Encompass));

         return View();
      }

      public ActionResult MlmLinkup()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(MlmLinkup));

         return View();
      }

      public ActionResult RedheadMobile()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(RedheadMobile));

         return View();
      }

      public ActionResult FamilyKey()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(FamilyKey));

         return View();
      }

      public ActionResult AzureServices()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(AzureServices));

         return View();
      }
   }
}