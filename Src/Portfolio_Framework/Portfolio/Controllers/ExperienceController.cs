using System.Web.Mvc;
using log4net;

namespace Portfolio.Controllers
{
   public class ExperienceController : Controller
   {
      #region Properties

      private readonly ILog _logger = LogManager.GetLogger(typeof(ExperienceController));

      #endregion

      public ActionResult Index()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Index));

         return View();
      }

      public ActionResult WorkHistory()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(WorkHistory));

         return View();
      }

      public ActionResult Education()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Education));

         return View();
      }
   }
}