using System.Web.Mvc;
using log4net;

namespace Portfolio.Controllers
{
	public class SkillsController : Controller
	{
      private readonly ILog _logger = LogManager.GetLogger(typeof(SkillsController));

      public ActionResult Index()
		{
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Index));

         return View();
		}

		public ActionResult Technologies()
		{
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Technologies));

         return View();
		}

		public ActionResult Leadership()
		{
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Leadership));

         return View();
		}

		public ActionResult CSharp()
		{
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(CSharp));

         return View();
		}

		public ActionResult Java()
		{
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Java));

         return View();
		}

		public ActionResult Database()
		{
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Database));

         return View();
		}

		public ActionResult Web()
		{
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(Web));

         return View();
		}

		public ActionResult VSTS()
		{
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(VSTS));

         return View();
		}

		public ActionResult WebApi()
		{
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(WebApi));

         return View();
		}

      public ActionResult CPlus()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(CPlus));

         return View();
      }

      public ActionResult QA()
      {
         _logger.DebugFormat("'{0}.{1}' called", GetType().Name, nameof(QA));

         return View();
      }
   }
}