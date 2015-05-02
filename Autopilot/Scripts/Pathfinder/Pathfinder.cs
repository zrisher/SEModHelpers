﻿#define LOG_ENABLED // remove on build

using Sandbox.ModAPI;
using System;
using System.Collections.Generic;
using VRage;
using VRageMath;

namespace Rynchodon.Autopilot.Pathfinder
{
	/// <summary>
	/// Finds alternate paths if the current path is blocked.
	/// </summary>
	internal class Pathfinder
	{
		private readonly IMyCubeGrid CubeGrid;

		private NavSettings CNS;
		private Vector3D Destination;// { get; private set; }
		private Vector3D? Waypoint;// { get; private set; }

		private IMyCubeGrid DestGrid;
		private IMyCubeBlock NavigationBlock;// { get; private set; }
		private bool IgnoreAsteroids;// { get; private set; }
		private bool NoAlternateRoute;// { get; private set; }

		private PathChecker myPathChecker;
		private static ThreadManager PathFinderThread = new ThreadManager();

		/// <summary>next time CheckPath() is allowed to run</summary>
		private DateTime nextRun = DateTime.MinValue;

		private Logger myLogger;

		public Pathfinder(IMyCubeGrid grid)
		{
			grid.throwIfNull_argument("grid");
			CubeGrid = grid;
			myPathChecker = new PathChecker(grid);
			myLogger = new Logger("Pathfinder", () => grid.DisplayName);
			myOutput = new PathfinderOutput(myPathChecker, PathfinderOutput.Result.Incomplete);
		}

		private PathfinderOutput myOutput;// = new PathfinderOutput(myPathChecker, PathfinderOutput.Result.Incomplete);
		private FastResourceLock lock_myOutput = new FastResourceLock();

		private void SetOutput(PathfinderOutput newOutput)
		{
			if (myPathChecker != null && myPathChecker.Interrupt)
				return;
			using (lock_myOutput.AcquireExclusiveUsing())
				myOutput = newOutput;
		}

		public PathfinderOutput GetOutput()
		{
			using (lock_myOutput.AcquireSharedUsing())
			{
				PathfinderOutput temp = myOutput;
				if (temp.PathfinderResult != PathfinderOutput.Result.Incomplete)
					myOutput = new PathfinderOutput(myPathChecker, PathfinderOutput.Result.Incomplete);
				return temp;
			}
		}

		internal void Run(NavSettings CNS, IMyCubeBlock NavigationBlock)
		{
			Vector3D destination = (Vector3D)CNS.getWayDest(false);
			Vector3D? waypoint = CNS.myWaypoint;
			bool ignoreAsteroids = CNS.ignoreAsteroids;
			bool noAlternateRoute = false;
			if (waypoint == destination)
				waypoint = null;

			// if something has changed, interrupt previous
			if (this.Destination != destination || this.Waypoint != waypoint || this.NavigationBlock != NavigationBlock || this.IgnoreAsteroids != ignoreAsteroids || this.NoAlternateRoute != noAlternateRoute || myOutput == null)
			{
				if (myPathChecker != null)
					myPathChecker.Interrupt = true;
				this.CNS = CNS;
				this.Destination = destination;
				this.Waypoint = waypoint;
				this.NavigationBlock = NavigationBlock;
				this.IgnoreAsteroids = ignoreAsteroids;
				this.NoAlternateRoute = noAlternateRoute;

				// decide whether to use collision avoidance or slowdown
				this.DestGrid = null;
				switch (CNS.getTypeOfWayDest())
				{
					case NavSettings.TypeOfWayDest.BLOCK:
					case NavSettings.TypeOfWayDest.GRID:
						// run slowdown. see Navigator.calcMoveAndRotate()
						this.DestGrid = CNS.CurrentGridDest.Grid;
						break;
					case NavSettings.TypeOfWayDest.LAND:
					default:
						if (CNS.landingState != NavSettings.LANDING.OFF && CNS.CurrentGridDest != null)
							this.DestGrid = CNS.CurrentGridDest.Grid;
						break;
				}
			}

			// not a race, this function is only called from one thread
			if (DateTime.UtcNow < nextRun)
				return;
			nextRun = DateTime.MaxValue;

			PathFinderThread.EnqueueAction(Wrapper_CheckPath);
		}

		private void Wrapper_CheckPath()
		{
			try
			{ CheckPath(); }
			catch (InterruptException)
			{ myLogger.debugLog("Caught Interrupt", "Wrapper_CheckPath", Logger.severity.DEBUG); }
			catch (Exception other)
			{ myLogger.debugLog("Exception: " + other, "Wrapper_CheckPath", Logger.severity.ERROR); }
			finally
			{
				if (myOutput != null && myOutput.PathfinderResult == PathfinderOutput.Result.No_Way_Forward)
				{
					myLogger.debugLog("no way forward, delaying next run by 60 seconds", "Wrapper_CheckPath()");
					nextRun = DateTime.UtcNow + new TimeSpan(0, 0, 60);
				}
				else
					nextRun = DateTime.UtcNow + new TimeSpan(0, 0, 1);
				//myLogger.debugLog("next run is in: " + nextRun, "Wrapper_CheckPath");
			}
		}

		private float DistanceToDest;

		private void CheckPath()
		{
			myLogger.debugLog("testing path to destination", "CheckPath()");
			Vector3? pointOfObstruction = null;
			Vector3D WayDest = Destination;
			DistanceToDest = (float)(Destination - NavigationBlock.GetPosition()).Length();

			IMyEntity ObstructingEntity = null;
			if (CNS.landingState == NavSettings.LANDING.OFF)
			{
				ObstructingEntity = myPathChecker.TestPath(RelativeVector3F.createFromWorldAbsolute(Destination, CubeGrid), NavigationBlock, IgnoreAsteroids, out pointOfObstruction, DestGrid);
				if (ObstructingEntity == null)
				{
					if (Waypoint == null)
					{
						myLogger.debugLog("Path to destination is clear", "CheckPath()", Logger.severity.DEBUG);
						SetOutput(new PathfinderOutput(myPathChecker, PathfinderOutput.Result.Path_Clear));
					}
					else
					{
						myLogger.debugLog("Re-routing to destination, path is now clear", "CheckPath()", Logger.severity.DEBUG);
						SetOutput(new PathfinderOutput(myPathChecker, PathfinderOutput.Result.Alternate_Path, null, Destination));
					}
					return;
				}
				CheckInterrupt();
				myLogger.debugLog("Path to destination is obstructed by " + ObstructingEntity.getBestName(), "CheckPath()", Logger.severity.DEBUG);
			}

			if (Waypoint != null)
			{
				WayDest = (Vector3)Waypoint;
				myLogger.debugLog("testing path to waypoint", "CheckPath()");
				ObstructingEntity = myPathChecker.TestPath(RelativeVector3F.createFromWorldAbsolute((Vector3D)Waypoint, CubeGrid), NavigationBlock, IgnoreAsteroids, out pointOfObstruction, DestGrid);
				if (ObstructingEntity == null)
				{
					myLogger.debugLog("Path to waypoint is clear", "CheckPath()", Logger.severity.DEBUG);
					SetOutput(new PathfinderOutput(myPathChecker, PathfinderOutput.Result.Path_Clear));
					return;
				}
			}

			if (ObstructingEntity == null)
			{
				myLogger.debugLog("Neither Destination nor Waypoint were tested", "CheckPath()", Logger.severity.DEBUG);
				return;
			}

			CheckInterrupt();
			if (NoAlternateRoute)
			{
				myLogger.debugLog("NoAlternateRoute, Obstruction = " + ObstructingEntity.getBestName(), "CheckPath()", Logger.severity.DEBUG);
				SetOutput(new PathfinderOutput(myPathChecker, PathfinderOutput.Result.No_Way_Forward, ObstructingEntity));
			}

			SetOutput(new PathfinderOutput(myPathChecker, PathfinderOutput.Result.Searching_Alt, ObstructingEntity));
			myLogger.debugLog("Path forward is obstructed by " + ObstructingEntity.getBestName() + " at " + pointOfObstruction, "CheckPath()", Logger.severity.TRACE);

			Vector3 lineToWayDest = WayDest - CubeGrid.GetCentre();
			Vector3 newPath_v1, newPath_v2;
			lineToWayDest.CalculatePerpendicularVector(out newPath_v1);
			newPath_v2 = lineToWayDest.Cross(newPath_v1);
			newPath_v1 = Vector3.Normalize(newPath_v1);
			newPath_v2 = Vector3.Normalize(newPath_v2);
			Vector3[] NewPathVectors = { newPath_v1, newPath_v2, Vector3.Negate(newPath_v1), Vector3.Negate(newPath_v2) };

			for (int newPathDistance = 8; newPathDistance < 10000; newPathDistance *= 2) // TODO: vet new point by verifying that we can move towards destination
			{
				myLogger.debugLog("newPathDistance = " + newPathDistance, "CheckPath()", Logger.severity.TRACE);

				// check far enough & sort alternate paths
				SortedDictionary<float, Vector3> Alternate_Path = new SortedDictionary<float, Vector3>();
				foreach (Vector3 PathVector in NewPathVectors)
				{
					pointOfObstruction.throwIfNull_variable("pointOfObstruction");
					Vector3 Alternate = (Vector3)pointOfObstruction + newPathDistance * PathVector;
					myLogger.debugLog("Alternate = " + Alternate, "CheckPath()");
					CNS.throwIfNull_variable("CNS");
					if (!CNS.waypointFarEnough(Alternate))
					{
						myLogger.debugLog("waypoint is too close, throwing out: " + Alternate, "CheckPath()");
						continue;
					}
					float distanceFromDest = Vector3.Distance(Destination, Alternate);
					Alternate_Path.throwIfNull_variable("Alternate_Path");
					while (Alternate_Path.ContainsKey(distanceFromDest))
						distanceFromDest = distanceFromDest.IncrementSignificand();
					Alternate_Path.Add(distanceFromDest, Alternate);

					//while (true)
					//{
					//	try
					//	{
					//		Alternate_Path.Add(distanceFromDest, Alternate);
					//		break;
					//	}
					//	catch (ArgumentException)
					//	{
					//		distanceFromDest = distanceFromDest.IncrementSignificand();
					//		myLogger.debugLog("Failed to add to Alternate_Path: " + distanceFromDest + ", " + Alternate, "CheckPath()");
					//	}
					//}
					myLogger.debugLog("Added alt path: " + Alternate + " with distance of " + distanceFromDest, "CheckPath()");
				}

				foreach (Vector3 AlternatePoint in Alternate_Path.Values)
					if (TestAltPath(AlternatePoint))
						return;
			}

			// before going to No Way Forward, check if we can move away from obstruction

			// try moving forward
			Vector3D GridCentre = CubeGrid.GetCentre();
			Vector3 Forward = NavigationBlock.WorldMatrix.Forward;
			for (int forwardDistance = 8 ; forwardDistance < 10000 ; forwardDistance *= 2)
			{
				Vector3 forwardPoint = GridCentre + forwardDistance * Forward;
				if (CNS.waypointFarEnough(forwardPoint))
				{
					myLogger.debugLog("testing forwards: forwardDistance = " + forwardDistance + ", forwardPoint = " + forwardPoint, "CheckPath()", Logger.severity.TRACE);
					if (TestAltPath(forwardPoint))
						return;
					break;
				}
				myLogger.debugLog("forwards too close: forwardDistance = " + forwardDistance + ", forwardPoint = " + forwardPoint, "CheckPath()", Logger.severity.TRACE);
			}

			SetOutput(new PathfinderOutput(myPathChecker, PathfinderOutput.Result.No_Way_Forward, ObstructingEntity));
			myLogger.debugLog("No Way Forward: " + ObstructingEntity.getBestName(), "CheckPath()", Logger.severity.INFO);

			//Vector3 Forward = Vector3.Normalize(lineToWayDest);
			Vector3 Backward = NavigationBlock.WorldMatrix.Backward;
			for (int backwardDistance = 8; backwardDistance < 10000; backwardDistance *= 2)
			{
				Vector3 backwardPoint = GridCentre + backwardDistance * Backward;
				if (CNS.waypointFarEnough(backwardPoint))
				{
					myLogger.debugLog("testing backwards: backwardDistance = " + backwardDistance + ", backwardPoint = " + backwardPoint, "CheckPath()", Logger.severity.TRACE);
					if (TestAltPath(backwardPoint))
						return;
					break;
				}
				myLogger.debugLog("backwards too close: backwardDistance = " + backwardDistance + ", backwardPoint = " + backwardPoint, "CheckPath()", Logger.severity.TRACE);
			}

			SetOutput(new PathfinderOutput(myPathChecker, PathfinderOutput.Result.No_Way_Forward, ObstructingEntity));
			myLogger.debugLog("No Way Forward: " + ObstructingEntity.getBestName(), "CheckPath()", Logger.severity.INFO);
		}

		///<summary>Test if a path can be flown. From current position to AlternatePoint</summary>
		/// <returns>true iff the path is flyable</returns>
		private bool TestAltPath(Vector3 AlternatePoint)
		{
			myLogger.debugLog("testing alternate path: " + AlternatePoint, "CheckPath()");
			Vector3? alt_pointOfObstruction;
			IMyEntity Alt_ObstructingEntity = myPathChecker.TestPath(RelativeVector3F.createFromWorldAbsolute(AlternatePoint, CubeGrid), NavigationBlock, IgnoreAsteroids, out alt_pointOfObstruction, DestGrid);
			if (Alt_ObstructingEntity == null) // found a new path
			{
				CheckInterrupt();

				// Is this a useful path; can we get closer to the destination by flying it?
				float pathwiseDistanceToDest = myPathChecker.distanceCanTravel(new Line(AlternatePoint, Destination));
				CheckInterrupt();

				if (pathwiseDistanceToDest >= DistanceToDest + CNS.destinationRadius)
				{
					myLogger.debugLog("path is unobstructed but not useful enough. distance to dest = " + DistanceToDest + ", pathwise = " + pathwiseDistanceToDest, "CheckPath()", Logger.severity.TRACE);
					CheckInterrupt();
					return false;
				}
				myLogger.debugLog("path is useful. distance to dest = " + DistanceToDest + ", pathwise = " + pathwiseDistanceToDest, "CheckPath()", Logger.severity.TRACE);

				SetOutput(new PathfinderOutput(myPathChecker, PathfinderOutput.Result.Alternate_Path, null, AlternatePoint));
				myLogger.debugLog("Found a new path: " + AlternatePoint, "CheckPath()", Logger.severity.DEBUG);
				return true;
			}
			myLogger.debugLog("Alternate path is obstructed by " + Alt_ObstructingEntity.getBestName() + " at " + alt_pointOfObstruction, "CheckPath()", Logger.severity.TRACE);
			CheckInterrupt();
			return false;
		}

		#region Interrupt

		/// <summary>
		/// throws an InterruptException if Interrupt
		/// </summary>
		private void CheckInterrupt()
		{
			if (myPathChecker.Interrupt)
				throw new InterruptException();
		}

		#endregion
	}
}