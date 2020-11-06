using System.Web.Mvc;
using log4net;

namespace Portfolio.Controllers
{
   public class FunProjectsController : Controller
   {
      #region Properties

      private readonly ILog _logger = LogManager.GetLogger(typeof(FunProjectsController));

      #endregion

      public ActionResult Index()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Index));

         return View();
      }

      public ActionResult HamRadioVHFGoKit()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Index));

         return View();
      }
   }
}