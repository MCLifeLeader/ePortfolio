using System.Web.Mvc;
using log4net;

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

		public ActionResult Contact()
		{
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Contact));

         return View();
		}

		public ActionResult Git()
		{
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Git));

         return View();
		}
	}
}