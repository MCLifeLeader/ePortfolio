using System.ComponentModel.DataAnnotations;

namespace Portfolio.Models
{
   /// <summary>
   /// This is a simple email message that contains no attachments.
   /// If this changes update the model in the Azure Function App
   /// </summary>
   public class EmailMessage
   {
      [EmailAddress(ErrorMessage = "Invalid Email Address")]
      [StringLength(250, ErrorMessage = "Email cannot be longer than 250 characters")]
      [Required(ErrorMessage = "Please Enter your Email Address")]
      public string FromAddress { get; set; }

      public string Subject { get; set; }
      
      [StringLength(2000, ErrorMessage = "Message cannot be longer than 2000 characters")]
      [Required(ErrorMessage = "Please Enter a Message")]
      public string MessageContent { get; set; }
   }
}