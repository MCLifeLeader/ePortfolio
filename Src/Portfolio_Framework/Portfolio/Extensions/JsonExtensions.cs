using System.Threading.Tasks;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Portfolio.Extensions
{
   public static class JsonExtensions
   {
      public static async Task<T> FromJsonAsync<T>(this string json)
      {
         return await Task.Run(() => JsonConvert.DeserializeObject<T>(json));
      }

      public static T FromJson<T>(this string json)
      {
         return FromJsonAsync<T>(json).GetAwaiter().GetResult();
      }

      public static async Task<string> ToJsonAsync(this object value)
      {
         return await Task.Run(() => JsonConvert.SerializeObject(value));
      }

      public static string ToJson(this object value)
      {
         return ToJsonAsync(value).GetAwaiter().GetResult();
      }

      /// <summary>
      /// Parses the json.
      /// </summary>
      /// <param name="json">The json.</param>
      /// <returns></returns>
      public static async Task<JObject> FromJsonToJObjectAsync(this string json)
      {
         if (string.IsNullOrEmpty(json))
         {
            return null;
         }

         return await Task.Run(() => JObject.Parse(json));
      }

      public static JObject FromJsonToJObject(this string json)
      {
         return FromJsonToJObjectAsync(json).GetAwaiter().GetResult();
      }

      /// <summary>
      /// Parses the json array.
      /// </summary>
      /// <param name="json">The json.</param>
      /// <returns></returns>
      public static async Task<JArray> FromJsonToJArrayAsync(this string json)
      {
         if (string.IsNullOrEmpty(json))
         {
            return null;
         }

         return await Task.Run(() => JArray.Parse(json));
      }

      public static JArray FromJsonToJArray(this string json)
      {
         return FromJsonToJArrayAsync(json).GetAwaiter().GetResult();
      }
   }
}