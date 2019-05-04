using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Portfolio.Models
{
   /// <summary>
   /// This is a simple email message that contains no attachments.
   /// </summary>
   public class EmailMessage
   {
      public string ToAddress { get; set; }
      public string FromAddress { get; set; }
      public string Subject { get; set; }
      public string MessageContent { get; set; }
   }
}